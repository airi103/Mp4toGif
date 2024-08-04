import os
import npyscreen

class MainForm(npyscreen.FormBaseNewWithMenus):
    def create(self):
        y, x = self.useable_space()
        max_width = max(40, x - 4)

        self.add(npyscreen.FixedText, value="Mp4ToGif", editable=False, rely=1, max_width=max_width)
        self.input_file = self.add(npyscreen.TitleFilenameCombo, name="Input:", rely=3, max_width=max_width)
        self.output_file = self.add(npyscreen.TitleText, name="Output:", rely=5, max_width=max_width)
        self.directory = self.add(npyscreen.TitleFilenameCombo, name="Dir:", rely=7, max_width=max_width)

        fps_values = ["10", "15", "24", "30", "60"]
        scale_values = ["480", "720", "1024", "1080", "1440", "2160"]

        self.fps = self.add(npyscreen.TitleSelectOne, name="FPS:", values=fps_values, max_height=3, scroll_exit=True, rely=9, max_width=max_width)
        self.scale = self.add(npyscreen.TitleSelectOne, name="Scale:", values=scale_values, max_height=3, scroll_exit=True, rely=13, max_width=max_width)

        button_y = min(y - 2, 17)
        execute_x = (max_width // 2) - 10
        cancel_x = (max_width // 2) + 2

        self.add(npyscreen.ButtonPress, name="Execute", rely=button_y, relx=execute_x, when_pressed_function=self.execute_commands)
        self.add(npyscreen.ButtonPress, name="Cancel", rely=button_y, relx=cancel_x, when_pressed_function=self.cancel)

    def execute_commands(self):
        input_file = self.input_file.value
        output_file = self.output_file.value
        directory = self.directory.value
        fps = self.fps.get_selected_objects()[0] if self.fps.value else None
        scale = self.scale.get_selected_objects()[0] if self.scale.value else None

        if not all([input_file, output_file, directory, fps, scale]):
            npyscreen.notify_confirm("All fields are required!", title="Error", wide=True)
            return

        try:
            os.chdir(directory)
        except OSError:
            npyscreen.notify_confirm("Invalid directory path!", title="Error", wide=True)
            return

        palette_cmd = f'ffmpeg -i "{input_file}" -vf "fps={fps},scale={scale}:-1:flags=lanczos,palettegen=reserve_transparent=1" -y palette.png'
        gif_cmd = f'ffmpeg -i "{input_file}" -i palette.png -filter_complex "fps={fps},scale={scale}:-1:flags=lanczos [v]; [v][1:v] paletteuse" -y "{output_file}"'

        if os.system(palette_cmd) != 0 or os.system(gif_cmd) != 0:
            npyscreen.notify_confirm("Error executing commands", title="Error", wide=True)
        else:
            npyscreen.notify_confirm("Commands executed successfully!", title="Success", wide=True)

    def cancel(self):
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

class Mp4ToGif(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, minimum_lines=19, minimum_columns=45)

if __name__ == "__main__":
    Mp4ToGif().run()
