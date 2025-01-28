#!/bin/python

if __name__ == "__main__":
    from aircommon import *
    
    import sys
    import os
    import PyQt6 as qt
    import PyQt6.QtWidgets as widgets
    
    fits_name_filter = "FITS files (*.fits *.fit)"
    
    class BiasWidget(widgets.QWidget):
        def __start_button_onpress(self):
            bias_files = self.bias_files
            outfile = self.masterbias_file_lineedit.text()
            
            if len(bias_files) == 0:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No bias files", "No bias files were submitted.")
                error_dialog.exec()
                return
            
            if outfile == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No master bias file", "No master bias file location has been entered.")
                error_dialog.exec()
                return
            
            notexists = []
            for bias_file in bias_files:
                if not os.path.isfile(bias_file):
                    notexists.append(bias_file)
            if any(notexists):
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "Bias files not found", "The following bias files were not found:\n" + "\n".join(notexists))
                error_dialog.exec()
                return
            
            if os.path.isfile(outfile):
                confirm_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Warning, "Master bias file already exists", f"The file {outfile} already exists. Do you want to overwrite it?", widgets.QMessageBox.StandardButton.No | widgets.QMessageBox.StandardButton.Yes)
                if confirm_dialog.exec() == widgets.QMessageBox.StandardButton.No.value:
                    return
            
            try:
                masterbias = create_masterbias_from_bias_files(bias_files)
                masterbias_header = create_masterheader_from_files(bias_files)
                write_fits_data(outfile, masterbias, header=masterbias_header)
                
                finish_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.NoIcon, "Done", "The master bias has been created.")
                finish_dialog.exec()
            except Exception as ex:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "An error occurred while creating the master bias", f"An error occurred:\n{ex}")
                error_dialog.exec()
        
        def __init__(self, parent):
            super().__init__()
            
            vlayout = widgets.QVBoxLayout()
            self.setLayout(vlayout)
            
            bias_files_selector, self.bias_files = parent.create_files_selector("bias")
            vlayout.addLayout(bias_files_selector)
            
            masterbias_file_selector, self.masterbias_file_lineedit = parent.create_file_selector("Master bias")
            vlayout.addLayout(masterbias_file_selector)
            
            start_hlayout = widgets.QHBoxLayout()
            vlayout.addLayout(start_hlayout)
            start_button = widgets.QPushButton("Start")
            start_button.clicked.connect(self.__start_button_onpress)
            start_hlayout.addWidget(start_button)
            start_hlayout.addStretch(1)
            
            vlayout.addStretch(1)
    
    class DarkWidget(widgets.QWidget):
        def __start_button_onpress(self):
            dark_files = self.dark_files
            bias_file = self.masterbias_file_lineedit.text()
            outfile = self.masterdark_file_lineedit.text()
            
            exposure_time_key = self.exposure_time_key_lineedit.text()
            gain_key = self.gain_key_lineedit.text()
            
            if len(dark_files) == 0:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No dark files", "No dark files were submitted.")
                error_dialog.exec()
                return
            
            if outfile == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No master dark file", "No master dark file location has been entered.")
                error_dialog.exec()
                return
            
            if exposure_time_key == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No exposure time key", "No exposure time key was given.")
                error_dialog.exec()
                return
            
            if gain_key == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No gain key", "No gain key was given.")
                error_dialog.exec()
                return
            
            notexists = []
            for dark_file in dark_files:
                if not os.path.isfile(dark_file):
                    notexists.append(dark_file)
            if any(notexists):
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "Dark files not found", "The following dark files were not found:\n" + "\n".join(notexists))
                error_dialog.exec()
                return
            
            if os.path.isfile(outfile):
                confirm_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Warning, "Master dark file already exists", f"The file {outfile} already exists. Do you want to overwrite it?", widgets.QMessageBox.StandardButton.No | widgets.QMessageBox.StandardButton.Yes)
                if confirm_dialog.exec() == widgets.QMessageBox.StandardButton.No.value:
                    return
            
            try:
                if bias_file:
                    masterbias = fits.getdata(bias_file)
                else:
                    masterbias = None
                masterdark = create_masterdark_from_dark_files(dark_files, masterbias=masterbias, exposure_time_key=exposure_time_key, gain_key=gain_key)
                masterdark_header = create_masterheader_from_files(dark_files)
                write_fits_data(outfile, masterdark, header=masterdark_header)
                
                finish_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.NoIcon, "Done", "The master dark has been created.")
                finish_dialog.exec()
            except Exception as ex:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "An error occurred while creating the master dark", f"An error occurred:\n{ex}")
                error_dialog.exec()
        
        def __init__(self, parent):
            super().__init__()
            
            self.dark_files = []
            
            hlayout = widgets.QHBoxLayout()
            self.setLayout(hlayout)
            
            vlayout_files = widgets.QVBoxLayout()
            hlayout.addLayout(vlayout_files)
            
            dark_files_selector, self.dark_files = parent.create_files_selector("dark")
            vlayout_files.addLayout(dark_files_selector)
            
            masterbias_file_selector, self.masterbias_file_lineedit = parent.create_file_selector("Master bias", must_exist=True)
            vlayout_files.addLayout(masterbias_file_selector)
            
            masterdark_file_selector, self.masterdark_file_lineedit = parent.create_file_selector("Master dark")
            vlayout_files.addLayout(masterdark_file_selector)
            
            start_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(start_hlayout)
            start_button = widgets.QPushButton("Start")
            start_button.clicked.connect(self.__start_button_onpress)
            start_hlayout.addWidget(start_button)
            start_hlayout.addStretch(1)
            
            vlayout_files.addStretch(1)
            
            vlayout_parameters = widgets.QVBoxLayout()
            hlayout.addLayout(vlayout_parameters)
            
            exposure_time_key_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(exposure_time_key_hlayout)
            exposure_time_key_label = widgets.QLabel("Exposure time key")
            exposure_time_key_hlayout.addWidget(exposure_time_key_label)
            self.exposure_time_key_lineedit = widgets.QLineEdit("EXPTIME")
            exposure_time_key_hlayout.addWidget(self.exposure_time_key_lineedit)
            exposure_time_key_hlayout.addStretch(1)
            
            gain_key_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(gain_key_hlayout)
            gain_key_label = widgets.QLabel("Gain key")
            gain_key_hlayout.addWidget(gain_key_label)
            self.gain_key_lineedit = widgets.QLineEdit("GAIN")
            gain_key_hlayout.addWidget(self.gain_key_lineedit)
            gain_key_hlayout.addStretch(1)
            
            vlayout_parameters.addStretch(1)
            
            hlayout.addStretch(1)
    
    class FlatWidget(widgets.QWidget):
        def __start_button_onpress(self):
            flat_files = self.flat_files
            bias_file = self.masterbias_file_lineedit.text()
            dark_file = self.masterdark_file_lineedit.text()
            outfile = self.masterflat_file_lineedit.text()
            
            exposure_time_key = self.exposure_time_key_lineedit.text()
            gain_key = self.gain_key_lineedit.text()
            rggb_componentwise = self.rggb_componentwise_checkbox.isChecked()
            
            if len(flat_files) == 0:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No flat files", "No flat files were submitted.")
                error_dialog.exec()
                return
            
            if outfile == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No master flat file", "No master flat file location has been entered.")
                error_dialog.exec()
                return
            
            if exposure_time_key == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No exposure time key", "No exposure time key was given.")
                error_dialog.exec()
                return
            
            if gain_key == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No gain key", "No gain key was given.")
                error_dialog.exec()
                return
            
            notexists = []
            for flat_file in flat_files:
                if not os.path.isfile(flat_file):
                    notexists.append(flat_file)
            if any(notexists):
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "Flat files not found", "The following flat files were not found:\n" + "\n".join(notexists))
                error_dialog.exec()
                return
            
            if os.path.isfile(outfile):
                confirm_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Warning, "Master flat file already exists", f"The file {outfile} already exists. Do you want to overwrite it?", widgets.QMessageBox.StandardButton.No | widgets.QMessageBox.StandardButton.Yes)
                if confirm_dialog.exec() == widgets.QMessageBox.StandardButton.No.value:
                    return
            
            try:
                if bias_file:
                    masterbias = fits.getdata(bias_file)
                else:
                    masterbias = None
                if dark_file:
                    masterdark = fits.getdata(dark_file)
                else:
                    masterdark = None
                masterflat = create_masterflat_from_flat_files(flat_files, masterbias=masterbias, masterdark=masterdark, exposure_time_key=exposure_time_key, gain_key=gain_key, rggb_componentwise=rggb_componentwise)
                masterflat_header = create_masterheader_from_files(flat_files)
                write_fits_data(outfile, masterflat, header=masterflat_header)
                
                finish_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.NoIcon, "Done", "The master flat has been created.")
                finish_dialog.exec()
            except Exception as ex:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "An error occurred while creating the master flat", f"An error occurred:\n{ex}")
                error_dialog.exec()
        
        def __init__(self, parent):
            super().__init__()
            
            hlayout = widgets.QHBoxLayout()
            self.setLayout(hlayout)
            
            vlayout_files = widgets.QVBoxLayout()
            hlayout.addLayout(vlayout_files)
            
            flat_files_selector, self.flat_files = parent.create_files_selector("flat")
            vlayout_files.addLayout(flat_files_selector)
            
            masterbias_file_selector, self.masterbias_file_lineedit = parent.create_file_selector("Master bias", must_exist=True)
            vlayout_files.addLayout(masterbias_file_selector)
            
            masterdark_file_selector, self.masterdark_file_lineedit = parent.create_file_selector("Master dark", must_exist=True)
            vlayout_files.addLayout(masterdark_file_selector)
            
            masterflat_file_selector, self.masterflat_file_lineedit = parent.create_file_selector("Master flat")
            vlayout_files.addLayout(masterflat_file_selector)
            
            start_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(start_hlayout)
            start_button = widgets.QPushButton("Start")
            start_button.clicked.connect(self.__start_button_onpress)
            start_hlayout.addWidget(start_button)
            start_hlayout.addStretch(1)
            
            vlayout_files.addStretch(1)
            
            vlayout_parameters = widgets.QVBoxLayout()
            hlayout.addLayout(vlayout_parameters)
            
            exposure_time_key_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(exposure_time_key_hlayout)
            exposure_time_key_label = widgets.QLabel("Exposure time key")
            exposure_time_key_hlayout.addWidget(exposure_time_key_label)
            self.exposure_time_key_lineedit = widgets.QLineEdit("EXPTIME")
            exposure_time_key_hlayout.addWidget(self.exposure_time_key_lineedit)
            exposure_time_key_hlayout.addStretch(1)
            
            gain_key_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(gain_key_hlayout)
            gain_key_label = widgets.QLabel("Gain key")
            gain_key_hlayout.addWidget(gain_key_label)
            self.gain_key_lineedit = widgets.QLineEdit("GAIN")
            gain_key_hlayout.addWidget(self.gain_key_lineedit)
            gain_key_hlayout.addStretch(1)
            
            rggb_componentwise_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(rggb_componentwise_hlayout)
            rggb_componentwise_label = widgets.QLabel("RGGB component wise")
            rggb_componentwise_hlayout.addWidget(rggb_componentwise_label)
            self.rggb_componentwise_checkbox = widgets.QCheckBox()
            rggb_componentwise_hlayout.addWidget(self.rggb_componentwise_checkbox)
            rggb_componentwise_hlayout.addStretch(1)
            
            vlayout_parameters.addStretch(1)
            
            hlayout.addStretch(1)
    
    class ScienceWidget(widgets.QWidget):
        def __start_button_onpress(self):
            light_files = self.light_files
            bias_file = self.masterbias_file_lineedit.text()
            dark_file = self.masterdark_file_lineedit.text()
            flat_file = self.masterflat_file_lineedit.text()
            outfolder = self.science_folder_lineedit.text()
            
            exposure_time_key = self.exposure_time_key_lineedit.text()
            gain_key = self.gain_key_lineedit.text()
            sky_subtraction = self.sky_subtraction_checkbox.isChecked()
            rggb_componentwise = self.rggb_componentwise_checkbox.isChecked()
            
            if len(light_files) == 0:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No light files", "No light files were submitted.")
                error_dialog.exec()
                return
            
            if outfolder == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No science output folder", "No science output folder has been entered.")
                error_dialog.exec()
                return
            
            if exposure_time_key == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No exposure time key", "No exposure time key was given.")
                error_dialog.exec()
                return
            
            if gain_key == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No gain key", "No gain key was given.")
                error_dialog.exec()
                return
            
            notexists = []
            alreadyexists = []
            outfiles = []
            for light_file in light_files:
                if not os.path.isfile(light_file):
                    notexists.append(light_file)
                filename = light_file.split("/")[-1]
                if filename.endswith(".fits"):
                    filename = filename[:-5]
                elif filename.endswith(".fit"):
                    filename = filename[:-4]
                outfile = outfolder + "/" + filename + ".Science.fits"
                if os.path.isfile(outfile):
                    alreadyexists.append(outfile)
                outfiles.append(outfile)
            if any(notexists):
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "Light files not found", "The following light files were not found:\n" + "\n".join(notexists))
                error_dialog.exec()
                return
            if any(alreadyexists):
                confirm_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Warning, "Science files already exist", "The following files already exist. Do you want to overwrite them?\n" + "\n".join(alreadyexists), widgets.QMessageBox.StandardButton.No | widgets.QMessageBox.StandardButton.Yes)
                if confirm_dialog.exec() == widgets.QMessageBox.StandardButton.No.value:
                    return
            
            try:
                if bias_file:
                    masterbias = fits.getdata(bias_file)
                else:
                    masterbias = None
                if dark_file:
                    masterdark = fits.getdata(dark_file)
                else:
                    masterdark = None
                if flat_file:
                    masterflat = fits.getdata(flat_file)
                else:
                    masterflat = None
                for i in range(len(light_files)):
                    science = create_science_from_light_file(light_files[i], masterbias=masterbias, masterdark=masterdark, masterflat=masterflat, exposure_time_key=exposure_time_key, gain_key=gain_key, do_sky_subtraction=sky_subtraction, rggb_componentwise=rggb_componentwise)
                    write_fits_data(outfiles[i], science, header=get_fits_header(light_files[i]))
                
                finish_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.NoIcon, "Done", "The sciences have been created.")
                finish_dialog.exec()
            except Exception as ex:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "An error occurred while creating the sciences", f"An error occurred:\n{ex}")
                error_dialog.exec()
        
        def __init__(self, parent):
            super().__init__()
            
            hlayout = widgets.QHBoxLayout()
            self.setLayout(hlayout)
            
            vlayout_files = widgets.QVBoxLayout()
            hlayout.addLayout(vlayout_files)
            
            light_files_selector, self.light_files = parent.create_files_selector("light")
            vlayout_files.addLayout(light_files_selector)
            
            masterbias_file_selector, self.masterbias_file_lineedit = parent.create_file_selector("Master bias", must_exist=True)
            vlayout_files.addLayout(masterbias_file_selector)
            
            masterdark_file_selector, self.masterdark_file_lineedit = parent.create_file_selector("Master dark", must_exist=True)
            vlayout_files.addLayout(masterdark_file_selector)
            
            masterflat_file_selector, self.masterflat_file_lineedit = parent.create_file_selector("Master flat", must_exist=True)
            vlayout_files.addLayout(masterflat_file_selector)
            
            science_folder_selector, self.science_folder_lineedit = parent.create_file_selector("Science folder", is_folder=True)
            vlayout_files.addLayout(science_folder_selector)
            
            start_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(start_hlayout)
            start_button = widgets.QPushButton("Start")
            start_button.clicked.connect(self.__start_button_onpress)
            start_hlayout.addWidget(start_button)
            start_hlayout.addStretch(1)
            
            vlayout_files.addStretch(1)
            
            vlayout_parameters = widgets.QVBoxLayout()
            hlayout.addLayout(vlayout_parameters)
            
            exposure_time_key_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(exposure_time_key_hlayout)
            exposure_time_key_label = widgets.QLabel("Exposure time key")
            exposure_time_key_hlayout.addWidget(exposure_time_key_label)
            self.exposure_time_key_lineedit = widgets.QLineEdit("EXPTIME")
            exposure_time_key_hlayout.addWidget(self.exposure_time_key_lineedit)
            exposure_time_key_hlayout.addStretch(1)
            
            gain_key_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(gain_key_hlayout)
            gain_key_label = widgets.QLabel("Gain key")
            gain_key_hlayout.addWidget(gain_key_label)
            self.gain_key_lineedit = widgets.QLineEdit("GAIN")
            gain_key_hlayout.addWidget(self.gain_key_lineedit)
            gain_key_hlayout.addStretch(1)
            
            sky_subtraction_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(sky_subtraction_hlayout)
            sky_subtraction_label = widgets.QLabel("Median sky subtraction")
            sky_subtraction_hlayout.addWidget(sky_subtraction_label)
            self.sky_subtraction_checkbox = widgets.QCheckBox()
            sky_subtraction_hlayout.addWidget(self.sky_subtraction_checkbox)
            sky_subtraction_hlayout.addStretch(1)
            
            rggb_componentwise_hlayout = widgets.QHBoxLayout()
            vlayout_parameters.addLayout(rggb_componentwise_hlayout)
            rggb_componentwise_label = widgets.QLabel("RGGB component wise")
            rggb_componentwise_hlayout.addWidget(rggb_componentwise_label)
            self.rggb_componentwise_checkbox = widgets.QCheckBox()
            rggb_componentwise_hlayout.addWidget(self.rggb_componentwise_checkbox)
            rggb_componentwise_hlayout.addStretch(1)
            
            vlayout_parameters.addStretch(1)
            
            hlayout.addStretch(1)
    
    class WCSWidget(widgets.QWidget):
        def __init__(self, parent):
            super().__init__()
    
    class MosaicWidget(widgets.QWidget):
        def __init__(self, parent):
            super().__init__()
    
    class MainWidget(widgets.QTabWidget):
        def __init__(self):
            super().__init__()
            
            self.addTab(BiasWidget, "Bias")
            self.addTab(DarkWidget, "Dark")
            self.addTab(FlatWidget, "Flat")
            self.addTab(ScienceWidget, "Science")
            self.addTab(WCSWidget, "WCS")
            self.addTab(MosaicWidget, "Mosaic")
        
        def addTab(self, widget, title):
            super().addTab(widget(self), title)
        
        def create_files_selector(self, filetype):
            files = []
            hlayout = widgets.QHBoxLayout()
            label = widgets.QLabel(f"{filetype[0].upper()}{filetype[1:]} files")
            hlayout.addWidget(label)
            button = widgets.QPushButton(f"Select {filetype} files...")
            button.clicked.connect(lambda: self.__selectfiles_button_onpress(label, filetype, files))
            hlayout.addWidget(button)
            hlayout.addStretch(1)
            return hlayout, files
        
        def create_file_selector(self, filetitle, is_folder=False, must_exist=False):
            hlayout = widgets.QHBoxLayout()
            label = widgets.QLabel(filetitle)
            hlayout.addWidget(label)
            lineedit = widgets.QLineEdit()
            hlayout.addWidget(lineedit)
            button = widgets.QPushButton("Select folder..." if is_folder else "Select file...")
            button.clicked.connect(lambda: self.__selectfile_button_onpress(lineedit, is_folder, must_exist))
            hlayout.addWidget(button)
            hlayout.addStretch(1)
            return hlayout, lineedit
        
        def __selectfiles_button_onpress(self, label, filetype, files_ref):
            files_dialog = widgets.QFileDialog(self)
            files_dialog.setNameFilter(fits_name_filter)
            files_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFiles)
            files_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptOpen)
            files_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if files_dialog.exec():
                files = files_dialog.selectedFiles()
                
                num = len(files)
                s = "s"
                if len(files) == 0:
                    num = "No"
                elif len(files) == 1:
                    s = ""
                label.setText(f"{num} {filetype} file{s} selected")
                
                files_ref[:] = files
        
        def __selectfile_button_onpress(self, lineedit, is_folder, must_exist):
            file_dialog = widgets.QFileDialog(self)
            if is_folder:
                file_dialog.setFileMode(widgets.QFileDialog.FileMode.Directory)
                file_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            else:
                file_dialog.setNameFilter(fits_name_filter)
                if must_exist:
                    file_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFile)
                    file_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptOpen)
                else:
                    file_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptSave)
                file_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if file_dialog.exec():
                lineedit.setText(file_dialog.selectedFiles()[0])
    
    app = widgets.QApplication(sys.argv)
    widget = MainWidget()
    widget.setWindowTitle("Astronomical Image Reducer")
    widget.setFixedSize(widget.sizeHint())
    widget.show()
    
    sys.exit(app.exec())