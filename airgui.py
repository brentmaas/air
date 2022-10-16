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
                self.biasfiles = files_dialog.selectedFiles()
                
                num = len(self.biasfiles)
                s = "s"
                if len(self.biasfiles) == 0:
                    num = "No"
                elif len(self.biasfiles) == 1:
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
            biasfiles = self.biasfiles
            outfile = self.outfile_file_lineedit.text()
            
            if len(biasfiles) == 0:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No bias files", "No bias files were submitted.")
                error_dialog.exec()
                return
            
            if outfile == "":
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "No master bias file", "No master bias file location has been entered.")
                error_dialog.exec()
                return
            
            notexists = []
            for biasfile in biasfiles:
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
                masterbias = create_masterbias_from_fits_files(biasfiles)
                write_fits_data(outfile, masterbias)
                
                finish_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.NoIcon, "Done", "The master bias has been created.")
                finish_dialog.exec()
            except Exception as ex:
                error_dialog = widgets.QMessageBox(widgets.QMessageBox.Icon.Critical, "An error occurred", f"An error occurred:\n{ex}")
                error_dialog.exec()
        
        def __init__(self):
            super().__init__()
            
            self.biasfiles = []
            
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
        def __init__(self):
            super().__init__()
    
    class FlatWidget(widgets.QWidget):
        def __init__(self):
            super().__init__()
    
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