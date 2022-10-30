if __name__ == "__main__":
    from aircommon import *
    
    import sys
    import os
    import PyQt6 as qt
    import PyQt6.QtWidgets as widgets
    
    fits_name_filter = "FITS files (*.fits *.fit)"
    
    class BiasWidget(widgets.QWidget):
        def __selectfiles_button_onpress(self):
            files_dialog = widgets.QFileDialog(self)
            files_dialog.setNameFilter(fits_name_filter)
            files_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFiles)
            files_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptOpen)
            files_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if files_dialog.exec():
                self.bias_files = files_dialog.selectedFiles()
                
                num = len(self.bias_files)
                s = "s"
                if len(self.bias_files) == 0:
                    num = "No"
                elif len(self.bias_files) == 1:
                    s = ""
                self.selectfiles_files_label.setText(f"{num} bias file{s} selected")
        
        def __outfile_button_onpress(self):
            file_dialog = widgets.QFileDialog(self)
            file_dialog.setNameFilter(fits_name_filter)
            file_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFile)
            file_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if file_dialog.exec():
                self.outfile_file_lineedit.setText(file_dialog.selectedFiles()[0])
        
        def __start_button_onpress(self):
            bias_files = self.bias_files
            outfile = self.outfile_file_lineedit.text()
            
            if len(bias_files) == 0:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No bias files", "No bias files were submitted.")
                error_dialog.exec()
                return
            
            if outfile == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No master bias file", "No master bias file location has been entered.")
                error_dialog.exec()
                return
            
            notexists = []
            for biasfile in bias_files:
                if not os.path.isfile(biasfile):
                    notexists.append(biasfile)
            if any(notexists):
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "Bias files not found", "The following bias files were not found:\n" + "\n".join(notexists))
                error_dialog.exec()
                return
            
            if os.path.isfile(outfile):
                confirm_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Warning, "Master bias file already exists", f"The file {outfile} already exists. Do you want to overwrite it?", widgets.QMessageBox.StandardButton.No | widgets.QMessageBox.StandardButton.Yes)
                if confirm_dialog.exec() == widgets.QMessageBox.StandardButton.No.value:
                    return
            
            try:
                masterbias = create_masterbias_from_fits_files(bias_files)
                write_fits_data(outfile, masterbias)
                
                finish_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.NoIcon, "Done", "The master bias has been created.")
                finish_dialog.exec()
            except Exception as ex:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "An error occurred while creating the master bias", f"An error occurred:\n{ex}")
                error_dialog.exec()
        
        def __init__(self):
            super().__init__()
            
            self.bias_files = []
            
            vlayout = widgets.QVBoxLayout()
            self.setLayout(vlayout)
            
            selectfiles_hlayout = widgets.QHBoxLayout()
            vlayout.addLayout(selectfiles_hlayout)
            selectfiles_input_label = widgets.QLabel("Bias files")
            selectfiles_hlayout.addWidget(selectfiles_input_label)
            selectfiles_button = widgets.QPushButton("Select bias files...")
            selectfiles_button.clicked.connect(self.__selectfiles_button_onpress)
            selectfiles_hlayout.addWidget(selectfiles_button)
            self.selectfiles_files_label = widgets.QLabel("No bias files selected")
            selectfiles_hlayout.addWidget(self.selectfiles_files_label)
            selectfiles_hlayout.addStretch(1)
            
            outfile_hlayout = widgets.QHBoxLayout()
            vlayout.addLayout(outfile_hlayout)
            outfile_output_label = widgets.QLabel("Master bias")
            outfile_hlayout.addWidget(outfile_output_label)
            self.outfile_file_lineedit = widgets.QLineEdit()
            outfile_hlayout.addWidget(self.outfile_file_lineedit)
            outfile_button = widgets.QPushButton("Select file...")
            outfile_button.clicked.connect(self.__outfile_button_onpress)
            outfile_hlayout.addWidget(outfile_button)
            outfile_hlayout.addStretch(1)
            
            start_hlayout = widgets.QHBoxLayout()
            vlayout.addLayout(start_hlayout)
            start_button = widgets.QPushButton("Start")
            start_button.clicked.connect(self.__start_button_onpress)
            start_hlayout.addWidget(start_button)
            start_hlayout.addStretch(1)
            
            vlayout.addStretch(1)
    
    class DarkWidget(widgets.QWidget):
        def __selectfiles_button_onpress(self):
            files_dialog = widgets.QFileDialog(self)
            files_dialog.setNameFilter(fits_name_filter)
            files_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFiles)
            files_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptOpen)
            files_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if files_dialog.exec():
                self.dark_files = files_dialog.selectedFiles()
                
                num = len(self.dark_files)
                s = "s"
                if len(self.dark_files) == 0:
                    num = "No"
                elif len(self.dark_files) == 1:
                    s = ""
                self.selectfiles_files_label.setText(f"{num} dark file{s} selected")
        
        def __selectbias_button_onpress(self):
            file_dialog = widgets.QFileDialog(self)
            file_dialog.setNameFilter(fits_name_filter)
            file_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFile)
            file_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if file_dialog.exec():
                self.selectbias_file_lineedit.setText(file_dialog.selectedFiles()[0])
        
        def __outfile_button_onpress(self):
            file_dialog = widgets.QFileDialog(self)
            file_dialog.setNameFilter(fits_name_filter)
            file_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFile)
            file_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if file_dialog.exec():
                self.outfile_file_lineedit.setText(file_dialog.selectedFiles()[0])
        
        def __start_button_onpress(self):
            dark_files = self.dark_files
            bias_file = self.selectbias_file_lineedit.text()
            outfile = self.outfile_file_lineedit.text()
            
            exposure_time_key = self.exposure_time_key_lineedit.text()
            gain_key = self.gain_key_lineedit.text()
            
            if len(dark_files) == 0:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No dark files", "No dark files were submitted.")
                error_dialog.exec()
                return
            
            if bias_file == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No master bias file", "No master bias file location has been entered.")
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
            for darkfile in dark_files:
                if not os.path.isfile(darkfile):
                    notexists.append(darkfile)
            if any(notexists):
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "Dark files not found", "The following dark files were not found:\n" + "\n".join(notexists))
                error_dialog.exec()
                return
            
            if os.path.isfile(outfile):
                confirm_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Warning, "Master dark file already exists", f"The file {outfile} already exists. Do you want to overwrite it?", widgets.QMessageBox.StandardButton.No | widgets.QMessageBox.StandardButton.Yes)
                if confirm_dialog.exec() == widgets.QMessageBox.StandardButton.No.value:
                    return
            
            try:
                masterdark = create_masterdark_from_fits_files(dark_files, exposure_time_key=exposure_time_key, gain_key=gain_key)
                write_fits_data(outfile, masterdark)
                
                finish_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.NoIcon, "Done", "The master dark has been created.")
                finish_dialog.exec()
            except Exception as ex:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "An error occurred while creating the master dark", f"An error occurred:\n{ex}")
                error_dialog.exec()
        
        def __init__(self):
            super().__init__()
            
            self.dark_files = []
            
            hlayout = widgets.QHBoxLayout()
            self.setLayout(hlayout)
            
            vlayout_files = widgets.QVBoxLayout()
            hlayout.addLayout(vlayout_files)
            
            selectfiles_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(selectfiles_hlayout)
            selectfiles_input_label = widgets.QLabel("Dark files")
            selectfiles_hlayout.addWidget(selectfiles_input_label)
            selectfiles_button = widgets.QPushButton("Select dark files...")
            selectfiles_button.clicked.connect(self.__selectfiles_button_onpress)
            selectfiles_hlayout.addWidget(selectfiles_button)
            self.selectfiles_files_label = widgets.QLabel("No dark files selected")
            selectfiles_hlayout.addWidget(self.selectfiles_files_label)
            selectfiles_hlayout.addStretch(1)
            
            selectbias_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(selectbias_hlayout)
            selectbias_input_label = widgets.QLabel("Master bias")
            selectbias_hlayout.addWidget(selectbias_input_label)
            self.selectbias_file_lineedit = widgets.QLineEdit()
            selectbias_hlayout.addWidget(self.selectbias_file_lineedit)
            selectbias_button = widgets.QPushButton("Select file...")
            selectbias_button.clicked.connect(self.__selectbias_button_onpress)
            selectbias_hlayout.addWidget(selectbias_button)
            selectfiles_hlayout.addStretch(1)
            
            outfile_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(outfile_hlayout)
            outfile_output_label = widgets.QLabel("Master dark")
            outfile_hlayout.addWidget(outfile_output_label)
            self.outfile_file_lineedit = widgets.QLineEdit()
            outfile_hlayout.addWidget(self.outfile_file_lineedit)
            outfile_button = widgets.QPushButton("Select file...")
            outfile_button.clicked.connect(self.__outfile_button_onpress)
            outfile_hlayout.addWidget(outfile_button)
            outfile_hlayout.addStretch(1)
            
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
        def __selectfiles_button_onpress(self):
            files_dialog = widgets.QFileDialog(self)
            files_dialog.setNameFilter(fits_name_filter)
            files_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFiles)
            files_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptOpen)
            files_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if files_dialog.exec():
                self.flat_files = files_dialog.selectedFiles()
                
                num = len(self.flat_files)
                s = "s"
                if len(self.flat_files) == 0:
                    num = "No"
                elif len(self.flat_files) == 1:
                    s = ""
                self.selectfiles_files_label.setText(f"{num} flat file{s} selected")
        
        def __selectbias_button_onpress(self):
            file_dialog = widgets.QFileDialog(self)
            file_dialog.setNameFilter(fits_name_filter)
            file_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFile)
            file_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if file_dialog.exec():
                self.selectbias_file_lineedit.setText(file_dialog.selectedFiles()[0])
        
        def __selectdark_button_onpress(self):
            file_dialog = widgets.QFileDialog(self)
            file_dialog.setNameFilter(fits_name_filter)
            file_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFile)
            file_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if file_dialog.exec():
                self.selectdark_file_lineedit.setText(file_dialog.selectedFiles()[0])
        
        def __outfile_button_onpress(self):
            file_dialog = widgets.QFileDialog(self)
            file_dialog.setNameFilter(fits_name_filter)
            file_dialog.setFileMode(widgets.QFileDialog.FileMode.ExistingFile)
            file_dialog.setAcceptMode(widgets.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setViewMode(widgets.QFileDialog.ViewMode.Detail)
            
            if file_dialog.exec():
                self.outfile_file_lineedit.setText(file_dialog.selectedFiles()[0])
        
        def __start_button_onpress(self):
            flat_files = self.flat_files
            bias_file = self.selectbias_file_lineedit.text()
            dark_file = self.selectdark_file_lineedit.text()
            outfile = self.outfile_file_lineedit.text()
            
            exposure_time_key = self.exposure_time_key_lineedit.text()
            gain_key = self.gain_key_lineedit.text()
            rggb_componentwise = self.rggb_componentwise_checkbox.isChecked()
            
            if len(flat_files) == 0:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No flat files", "No flat files were submitted.")
                error_dialog.exec()
                return
            
            if bias_file == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No master bias file", "No master bias file location has been entered.")
                error_dialog.exec()
                return
            
            if dark_file == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No master dark file", "No master dark file location has been entered.")
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
            for flatfile in flat_files:
                if not os.path.isfile(flatfile):
                    notexists.append(flatfile)
            if any(notexists):
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "Flat files not found", "The following flat files were not found:\n" + "\n".join(notexists))
                error_dialog.exec()
                return
            
            if os.path.isfile(outfile):
                confirm_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Warning, "Master flat file already exists", f"The file {outfile} already exists. Do you want to overwrite it?", widgets.QMessageBox.StandardButton.No | widgets.QMessageBox.StandardButton.Yes)
                if confirm_dialog.exec() == widgets.QMessageBox.StandardButton.No.value:
                    return
            
            try:
                masterflat = create_masterflat_from_fits_files(flat_files, exposure_time_key=exposure_time_key, gain_key=gain_key, rggb_componentwise=rggb_componentwise)
                write_fits_data(outfile, masterflat)
                
                finish_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.NoIcon, "Done", "The master flat has been created.")
                finish_dialog.exec()
            except Exception as ex:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "An error occurred while creating the master flat", f"An error occurred:\n{ex}")
                error_dialog.exec()
        
        def __init__(self):
            super().__init__()
            
            self.flat_files = []
            
            hlayout = widgets.QHBoxLayout()
            self.setLayout(hlayout)
            
            vlayout_files = widgets.QVBoxLayout()
            hlayout.addLayout(vlayout_files)
            
            selectfiles_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(selectfiles_hlayout)
            selectfiles_input_label = widgets.QLabel("Flat files")
            selectfiles_hlayout.addWidget(selectfiles_input_label)
            selectfiles_button = widgets.QPushButton("Select flat files...")
            selectfiles_button.clicked.connect(self.__selectfiles_button_onpress)
            selectfiles_hlayout.addWidget(selectfiles_button)
            self.selectfiles_files_label = widgets.QLabel("No flat files selected")
            selectfiles_hlayout.addWidget(self.selectfiles_files_label)
            selectfiles_hlayout.addStretch(1)
            
            selectbias_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(selectbias_hlayout)
            selectbias_input_label = widgets.QLabel("Master bias")
            selectbias_hlayout.addWidget(selectbias_input_label)
            self.selectbias_file_lineedit = widgets.QLineEdit()
            selectbias_hlayout.addWidget(self.selectbias_file_lineedit)
            selectbias_button = widgets.QPushButton("Select file...")
            selectbias_button.clicked.connect(self.__selectbias_button_onpress)
            selectbias_hlayout.addWidget(selectbias_button)
            selectfiles_hlayout.addStretch(1)
            
            selectdark_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(selectdark_hlayout)
            selectdark_input_label = widgets.QLabel("Master dark")
            selectdark_hlayout.addWidget(selectdark_input_label)
            self.selectdark_file_lineedit = widgets.QLineEdit()
            selectdark_hlayout.addWidget(self.selectdark_file_lineedit)
            selectdark_button = widgets.QPushButton("Select file...")
            selectdark_button.clicked.connect(self.__selectdark_button_onpress)
            selectdark_hlayout.addWidget(selectdark_button)
            selectfiles_hlayout.addStretch(1)
            
            outfile_hlayout = widgets.QHBoxLayout()
            vlayout_files.addLayout(outfile_hlayout)
            outfile_output_label = widgets.QLabel("Master flat")
            outfile_hlayout.addWidget(outfile_output_label)
            self.outfile_file_lineedit = widgets.QLineEdit()
            outfile_hlayout.addWidget(self.outfile_file_lineedit)
            outfile_button = widgets.QPushButton("Select file...")
            outfile_button.clicked.connect(self.__outfile_button_onpress)
            outfile_hlayout.addWidget(outfile_button)
            outfile_hlayout.addStretch(1)
            
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
        def __init__(self):
            super().__init__()
    
    class WCSWidget(widgets.QWidget):
        def __init__(self):
            super().__init__()
    
    class MosaicWidget(widgets.QWidget):
        def __init__(self):
            super().__init__()
    
    app = widgets.QApplication(sys.argv)
    widget = widgets.QTabWidget()
    
    bias_widget = BiasWidget()
    widget.addTab(bias_widget, "Bias")
    
    dark_widget = DarkWidget()
    widget.addTab(dark_widget, "Dark")
    
    flat_widget = FlatWidget()
    widget.addTab(flat_widget, "Flat")
    
    science_widget = ScienceWidget()
    widget.addTab(science_widget, "Science")
    
    wcs_widget = WCSWidget()
    widget.addTab(wcs_widget, "WCS")
    
    mosaic_widget = MosaicWidget()
    widget.addTab(mosaic_widget, "Mosaic")
    
    widget.setWindowTitle("Astronomical Image Reducer")
    widget.setFixedSize(widget.sizeHint())
    widget.show()
    sys.exit(app.exec())