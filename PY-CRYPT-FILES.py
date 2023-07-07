import sys
import random
import string
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class FileEncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Encryption App")
        self.setFixedSize(600, 200)

        # Estilo da janela
        self.setStyleSheet("background-color: white; color: black;")

        # Criação dos elementos da interface
        self.file_label = QLabel("Arquivo:", self)
        self.file_path_label = QLabel("", self)
        self.file_path_label.setWordWrap(True)
        self.file_path_label.setAlignment(Qt.AlignTop)
        self.select_file_button = QPushButton("Selecionar Arquivo", self)
        self.select_file_button.setStyleSheet("background-color: #0088FF; color: white;")
        self.password_label = QLabel("Senha:", self)
        self.password_input = QLineEdit(self)
        self.generate_password_button = QPushButton("Gerar Senha", self)
        self.generate_password_button.setStyleSheet("background-color: #0088FF; color: white;")
        self.encrypt_button = QPushButton("Criptografar", self)
        self.encrypt_button.setStyleSheet("background-color: #0088FF; color: white;")
        self.decrypt_button = QPushButton("Descriptografar", self)
        self.decrypt_button.setStyleSheet("background-color: #0088FF; color: white;")

        # Configuração do layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.generate_password_button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        self.setLayout(layout)

        # Conexão dos botões com as funções correspondentes
        self.select_file_button.clicked.connect(self.select_file)
        self.generate_password_button.clicked.connect(self.generate_password)
        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.decrypt_button.clicked.connect(self.decrypt_file)

        # Gerar chave RSA
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecionar Arquivo")
        if file_path:
            self.file_path_label.setText(file_path)

    def generate_password(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=128))
        self.password_input.setText(password)

    def encrypt_file(self):
        file_path = self.file_path_label.text()
        password = self.password_input.text().encode()

        if not file_path:
            self.show_message("Erro", "Nenhum arquivo selecionado.")
            return

        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Gerar chave simétrica
            symmetric_key = self.generate_symmetric_key()

            # Criptografar o conteúdo do arquivo usando a chave simétrica
            encrypted_content = self.encrypt_content(file_content, symmetric_key)

            # Criptografar a chave simétrica usando a chave pública RSA
            encrypted_key = self.encrypt_key(symmetric_key)

            # Salvar o arquivo criptografado com a extensão .cryptfile
            output_file_path = self.get_output_file_path(file_path)
            self.save_encrypted_file(output_file_path, encrypted_key, encrypted_content)

            self.show_message("Sucesso", "Arquivo criptografado com sucesso.\nArquivo salvo como: " + output_file_path)

        except Exception as e:
            self.show_message("Erro", "Ocorreu um erro ao criptografar o arquivo:\n" + str(e))

    def decrypt_file(self):
        file_path = self.file_path_label.text()
        password = self.password_input.text().encode()

        if not file_path:
            self.show_message("Erro", "Nenhum arquivo selecionado.")
            return

        if not file_path.endswith(".cryptfile"):
            self.show_message("Erro", "O arquivo selecionado não é um arquivo criptografado.")
            return

        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Descriptografar a chave simétrica usando a chave privada RSA
            symmetric_key = self.decrypt_key(file_content)

            # Descriptografar o conteúdo do arquivo usando a chave simétrica
            decrypted_content = self.decrypt_content(file_content, symmetric_key)

            # Salvar o arquivo descriptografado com o nome original
            output_file_path = self.get_output_file_path(file_path)
            self.save_decrypted_file(output_file_path, decrypted_content)

            self.show_message("Sucesso", "Arquivo descriptografado com sucesso.\nArquivo salvo como: " + output_file_path)

        except Exception as e:
            self.show_message("Erro", "Ocorreu um erro ao descriptografar o arquivo:\n" + str(e))

    def generate_symmetric_key(self):
        return os.urandom(32)

    def encrypt_content(self, content, key):
        cipher = Cipher(algorithms.AES(key), modes.GCM())
        encryptor = cipher.encryptor()
        encrypted_content = encryptor.update(content) + encryptor.finalize()
        return encrypted_content

    def decrypt_content(self, content, key):
        cipher = Cipher(algorithms.AES(key), modes.GCM())
        decryptor = cipher.decryptor()
        decrypted_content = decryptor.update(content) + decryptor.finalize()
        return decrypted_content

    def encrypt_key(self, key):
        encrypted_key = self.private_key.public_key().encrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_key

    def decrypt_key(self, encrypted_key):
        decrypted_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_key

    def get_output_file_path(self, file_path):
        return file_path + ".cryptfile"

    def save_encrypted_file(self, output_file_path, encrypted_key, encrypted_content):
        with open(output_file_path, 'wb') as output_file:
            output_file.write(encrypted_key + b"|" + encrypted_content)

    def save_decrypted_file(self, output_file_path, decrypted_content):
        with open(output_file_path, 'wb') as output_file:
            output_file.write(decrypted_content)

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Estilo da aplicação
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(245, 245, 245))
    palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(0, 136, 255))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

    font = QFont()
    font.setPointSize(10)
    app.setFont(font)

    file_encryption_app = FileEncryptionApp()
    file_encryption_app.show()
    sys.exit(app.exec_())
