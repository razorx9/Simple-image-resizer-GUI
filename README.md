# Simple image resizer GUI 🙂

A simple GUI interface made with [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter) to do image resizing. Image resizing is done using the `pillow` library.

### App UI
![](/readme_docs/app_window.png)


### known issue:
Stops process and output error if non-image files are present in the selected directory. Will rectify this in the future update, maybe?



### Packaging (Windows PyInstaller): 
_(copied from [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter) page.)_

When you create a .exe on Windows with pyinstaller, there are two things you have to consider. Firstly, you cannot use the `--onefile` option of pyinstaller, because the customtkinter library includes not only .py files, but also data files like .json and .otf. PyInstaller is not able to pack them into a single .exe file, so you have to use the `--onedir` option.

And secondly, you have to include the customtkinter directory manually with the `--add-data` option of pyinstaller. Because for some reason, pyinstaller doesn't automatically include datafiles like .json from the library. You can find the install location of the customtkinter library with the following command:

```
pip show customtkinter
```
A Location will be shown, for example: `c:\users\<user_name>\appdata\local\programs\python\python310\lib\site-packages`

Then add the library folder like this:`--add-data "C:/Users/<user_name>/AppData/Local/Programs/Python/Python310/Lib/site-packages/customtkinter;customtkinter/"`

For the full command you get something like this:
```
pyinstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "<Path to Python Script>"
```
