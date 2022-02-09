import sys

from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QTransform, QPalette, QImage
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, QStatusBar, QToolBar, QDockWidget, QPushButton, \
    QVBoxLayout, QLabel, QSizePolicy, QFileDialog, QMessageBox, QDesktopWidget, QSlider, QScrollArea


class MyPhotoEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        self.setFixedSize(700, 700)
        self.setWindowTitle("My First Photo Editor")
        self.zoom_factor = 1
        self.center_main_window()
        self.tools_dock_widget()
        self.create_menu()
        self.create_toolbar()
        self.editors_widgets()
        self.show()

    def create_menu(self):
        # Actions for file menu
        self.open_file = QAction(QIcon("images/open.png"), "Open", self)
        self.open_file.setShortcut("Ctrl + O")
        self.open_file.setStatusTip("Open new image")
        self.open_file.triggered.connect(self.open_image)

        self.save_file = QAction(QIcon("images/save.jpeg"), "Save", self)
        self.save_file.setShortcut("Ctrl + S")
        self.save_file.setStatusTip("Saving Image")
        self.save_file.triggered.connect(self.save_image)

        self.print_file = QAction(QIcon("images/print.jpeg"), "Print", self)
        self.print_file.setShortcut("Ctrl + P")
        self.print_file.setStatusTip("Print Image")
        self.print_file.triggered.connect(self.print_image)
        self.print_file.setEnabled(False)

        self.exit_file = QAction(QIcon("images/exit.jpeg"), "Exit", self)
        self.exit_file.setShortcut("Ctrl + Q")
        self.exit_file.setStatusTip("Quit program")
        self.exit_file.triggered.connect(self.close)

        # Actions for edit menu
        self.rotate_90 = QAction(QIcon("images/rotate 90.png"), "Rotate 90º", self)
        self.rotate_90.setStatusTip("Rotate image 90º clockwise")
        self.rotate_90.triggered.connect(self.rotate_90_image)

        self.rotate_180 = QAction(QIcon("images/rotate 180.png"), "Rotate 180º", self)
        self.rotate_180.setStatusTip("Rotate image 180º clockwise")
        self.rotate_180.triggered.connect(self.rotate_180_image)

        self.flip_horizontal = QAction(QIcon("images/flip horizontally.png"), "Flip Image Horizontally", self)
        self.flip_horizontal.setStatusTip("Flip image across horizontal axis")
        self.flip_horizontal.triggered.connect(self.flip_horizontal_image)

        self.flip_vertical = QAction(QIcon("images/flip vertically.png"), "Flip Image Vertically", self)
        self.flip_vertical.setStatusTip("Flip image across vertical axis")
        self.flip_vertical.triggered.connect(self.flip_vertical_image)

        self.resize_file = QAction(QIcon("images/resize.png"), "Resize Image", self)
        self.resize_file.setStatusTip("Resize image to half the original size")
        self.resize_file.triggered.connect(self.resize_image)

        self.clear_file = QAction(QIcon("images/clear.jpeg"), "Clear Image", self)
        self.clear_file.setShortcut("Ctrl + D")
        self.clear_file.setStatusTip("Clear Current Image")
        self.clear_file.triggered.connect(self.clear_image)

        self.crop_file = QAction(QIcon("images/crop.png"), "Crop File", self)
        self.crop_file.setShortcut("Shift + X")
        self.crop_file.setStatusTip("Crop File")
        self.crop_file.triggered.connect(self.crop_image)

        self.zoom_in_act = QAction(QIcon("images/zoom in.jpeg"), "Zoom In Image", self)
        self.zoom_in_act.setStatusTip("Zoom In Image")
        self.zoom_in_act.triggered.connect(lambda: self.zoom_on_image(1.25))
        self.zoom_in_act.setEnabled(False)

        self.zoom_out_act = QAction(QIcon("images/zoom out.jpeg"), "Zoom Out Image", self)
        self.zoom_out_act.setStatusTip("Zoom Out Image")
        self.zoom_out_act.triggered.connect(lambda:self.zoom_on_image(0.8))
        self.zoom_out_act.setEnabled(False)

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.scroll_area)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Creating File menu and Adding actions
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self.open_file)
        file_menu.addAction(self.save_file)
        file_menu.addSeparator()
        file_menu.addAction(self.print_file)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_file)

        # Creating Edit menu and Actions
        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction(self.rotate_90)
        edit_menu.addAction(self.rotate_180)
        edit_menu.addSeparator()
        edit_menu.addAction(self.flip_horizontal)
        edit_menu.addAction(self.flip_vertical)
        edit_menu.addSeparator()
        edit_menu.addAction(self.resize_file)
        edit_menu.addSeparator()
        edit_menu.addAction(self.zoom_in_act)
        edit_menu.addAction(self.zoom_out_act)
        edit_menu.addSeparator()
        edit_menu.addAction(self.clear_file)

        # View menu and Add actions
        view_menu = menu_bar.addMenu("View")
        view_menu.addAction(self.docks_tools)

        self.setStatusBar(QStatusBar(self))

    def create_toolbar(self):
        tool_bar = QToolBar("Editor Toolbar")
        tool_bar.setIconSize(QSize(30, 30))
        self.addToolBar(tool_bar)

        # adding actions to toolbar
        tool_bar.addAction(self.open_file)
        tool_bar.addAction(self.save_file)
        tool_bar.addSeparator()
        tool_bar.addAction(self.print_file)
        tool_bar.addAction(self.clear_file)
        tool_bar.addSeparator()
        tool_bar.addAction(self.crop_file)
        tool_bar.addAction(self.exit_file)

    def tools_dock_widget(self):
        self.dock_tools_view = QDockWidget()
        self.dock_tools_view.setWindowTitle("Edit Image Tools")
        self.dock_tools_view.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.tools_contents = QWidget()

        self.rotate_90 = QPushButton("Rotate 90º")
        self.rotate_90.setMinimumSize(QSize(130, 40))
        self.rotate_90.setStatusTip("Rotate image 90º clockwise")
        self.rotate_90.clicked.connect(self.rotate_90_image)

        self.rotate_180 = QPushButton("Rotate 180º")
        self.rotate_180.setMinimumSize(QSize(130, 40))
        self.rotate_180.setStatusTip("Rotate image 180º clockwise")
        self.rotate_180.clicked.connect(self.rotate_180_image)

        self.flip_horizontal = QPushButton("Flip Horizontal")
        self.flip_horizontal.setMinimumSize(130, 40)
        self.flip_horizontal.setStatusTip("Flip image across horizontal axis")
        self.flip_horizontal.clicked.connect(self.flip_horizontal_image)

        self.flip_vertical = QPushButton("Flip Vertical")
        self.flip_vertical.setMinimumSize(130, 40)
        self.flip_vertical.setStatusTip("Flip image across vertical axis")
        self.flip_vertical.clicked.connect(self.flip_vertical_image)

        self.resize_file = QPushButton("Resize Half")
        self.resize_file.setMinimumSize(130, 40)
        self.resize_file.setStatusTip("Resize image to half the original size")
        self.resize_file.clicked.connect(self.resize_image)

        self.zoom_in_act = QPushButton("Zoom In")
        self.zoom_in_act.setMinimumSize(130, 40)
        self.zoom_in_act.clicked.connect(self.zoom_on_image)

        self.zoom_out_act = QPushButton("Zoom Out")
        self.zoom_out_act.setMinimumSize(130, 40)
        self.zoom_out_act.clicked.connect(self.zoom_on_image)

        self.crop_file = QPushButton("Crop Image")
        self.crop_file.setMinimumSize(130, 40)
        self.crop_file.clicked.connect(self.crop_image)

        v_box = QVBoxLayout()
        v_box.addWidget(self.rotate_90)
        v_box.addWidget(self.rotate_180)
        v_box.addStretch(1)
        v_box.addWidget(self.flip_horizontal)
        v_box.addWidget(self.flip_vertical)
        v_box.addStretch(1)
        v_box.addWidget(self.zoom_in_act)
        v_box.addWidget(self.zoom_out_act)
        v_box.addStretch(1)
        v_box.addWidget(self.resize_file)
        v_box.addWidget(self.crop_file)
        v_box.addStretch(6)

        self.tools_contents.setLayout(v_box)
        self.dock_tools_view.setWidget(self.tools_contents)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_tools_view)
        self.docks_tools = self.dock_tools_view.toggleViewAction()

    def editors_widgets(self):
        self.image = QPixmap()
        self.image_label = QLabel()

        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)

        self.setCentralWidget(self.image_label)

    def open_image(self):
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "JPG Files (*.jpeg *.jpg )"
                                                                            ";;PNG Files (*.png);;Bitmap Files ("
                                                                            "*.bmp);;GIF Files (*.gif)")
        if image_file:
            self.image = QPixmap(image_file)
            self.image_label.setPixmap(self.image.scaled(self.image_label.size(),
                                                         Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            QMessageBox.information(self, "Error", "Unable to open image!", QMessageBox.Ok)

        self.print_file.setEnabled(True)

    def save_image(self):
        image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                    "JPG Files (*.jpeg *.jpg );;PNG Files (*.png)"
                                                    ";;Bitmap Files (*.bmp);;\GIF Files (*.gif)")
        if image_file and self.image.isNull() == False:
            self.image.save(image_file)
        else:
            QMessageBox.information(self, "Error", "Unable to save image!", QMessageBox.Ok)

    def print_image(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.NativeFormat)

        print_dialog = QPrintDialog(printer)

        if print_dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            painter.begin(printer)
            rect = QRect(painter.viewport())
            size = QSize(self.image_label.pixmap().size())
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image_label.pixmap().rect())
            painter.drawPixmap(0, 0, self.image_label.pixmap())
            painter.end()

    def rotate_90_image(self):
        if self.image.isNull() == False:
            transform90 = QTransform().rotate(90)
            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)
            self.image_label.setPixmap(rotated.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(rotated)
            self.image_label.repaint()
        else:
            pass

    def rotate_180_image(self):
        if self.image.isNull() == False:
            transform180 = QTransform().rotate(180)
            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform180, mode=Qt.SmoothTransformation)

            self.image_label.setPixmap(rotated.scaled(self.image_label.size(),
                                                      Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(rotated)
            self.image_label.repaint()
        else:
            pass

    def flip_horizontal_image(self):
        if self.image.isNull() == False:
            flip_h = QTransform().scale(-1, 1)
            pixmap = QPixmap(self.image)

            flipped = pixmap.transformed(flip_h)

            self.image_label.setPixmap(flipped.scaled(self.image_label.size(),
                                                      Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(flipped)
            self.image_label.repaint()
        else:
            pass

    def flip_vertical_image(self):
        if self.image.isNull() == False:
            flip_v = QTransform().scale(1, -1)
            pixmap = QPixmap(self.image)

            flipped = pixmap.transformed(flip_v)

            self.image_label.setPixmap(flipped.scaled(self.image_label.size(),
                                                      Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(flipped)
            self.image_label.repaint()
        else:
            pass

    def resize_image(self):
        if self.image.isNull() == False:
            resize = QTransform().scale(0.5, 0.5)
            pixmap = QPixmap(self.image)

            resized = pixmap.transformed(resize)

            self.image_label.setPixmap(resized.scaled(self.image_label.size(),
                                                      Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(resized)
            self.image_label.repaint()
        else:
            pass

    def clear_image(self):
        self.image_label.clear()
        self.image = QPixmap()

    def center_main_window(self):
        desktop = QDesktopWidget().screenGeometry()
        screen_width = desktop.width()
        screen_height = desktop.height()

        self.move((screen_width - self.width()) / 2, (screen_height - self.height()) / 2)

    def crop_image(self):
        if self.image.isNull() == False:
            rect = QRect(10, 20, 400, 200)
            original_image = self.image
            cropped = original_image.copy(rect)

            self.image = QImage(cropped)
            self.setPixmap(QPixmap().fromImage(cropped))

    def zoom_on_image(self, zoom_value):
        self.zoom_factor *= zoom_value
        self.image_label.resize(self.zoom_factor * self.image_label.pixmap().size())

        self.adjustScrollBar(self.scroll_area.horizontalScrollBar(), zoom_value)
        self.adjustScrollBar(self.scroll_area.verticalScrollBar(), zoom_value)

        self.zoom_in_act.setEnabled(self.zoom_factor < 4.0)
        self.zoom_out_act.setEnabled(self.zoom_factor > 0.333)

        self.scroll_area.setWidget(self.image_label)

    def normal_size(self):
        """View image with its normal dimensions."""
        self.image_label.adjustSize()
        self.zoom_factor = 1.0

    def adjustScrollBar(self, scroll_bar, value):
        """Adjust the scrollbar when zooming in or out."""
        scroll_bar.setValue(int(value * scroll_bar.value()) + ((value - 1) * scroll_bar.pageStep() / 2))


stylesheet = """
    QWidget {
        background-color: #D3E9F0;
        color: #1A7B9E;
        border: 2px solid black
    }   
        QPushButton {
        background-color: #B7B7F2;
        color: #3838EB;
        border: 2px solid black
        }     
 """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = MyPhotoEditor()
    sys.exit(app.exec_())
