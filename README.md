# CRYPt

Encrypt txt files with a dash of "salt" and yor password. 

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Instructions for running it alone:

Make sure to download python with dootenv and cryptography libraries. Place 2 python codes in one directory together with the txt file you want to encrypt and make .env file that contains:

password=YOURPASSWORD      

which is gonna be used for encrypting and decrypting your file. After everything is in order open your terminal in your directory and run 

python encrypt_secure.py yourfile.txt 

which will create a new file yourfile.txt.encrypted. You can run that file back to decrypt it with the command 

python decrypt_secure.py yourfile.txt.encrypted

and that will output your file decrypted if the password and "Salt" matches.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

If you wanna run it with .bat file included place all of the code in this arrangment.

yourdirectory
  I-> CRYPt.bat - shortcut
  I-> files
       I-> encrypt_secure.py
       I-> decrypt_secure.py
       I-> CRYPt.bat


Just make sure you have pip installed and run CRYPt.bat shortcut. File will download needed libraries automatically if you have pip installed. You can open further instruction in the .bat file itself. 
