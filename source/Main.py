import tkinter
import pygubu

from source.DatasetParser import Parser


class Application(pygubu.TkApplication):
    def _create_ui(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file("../ui/parser_ui.ui")
        self.mainwindow = builder.get_object("mainwindow", self.master)
        self.set_title("Dataset Parser")

        self.parser = Parser()

        callbacks = {
            "create_parse": self.createparse,
            # "create_wordset": self.createwordset,
            # "create_charset": self.createcharset,
            "create_dict": self.createdict
        }

        builder.connect_callbacks(callbacks)

        self.dataset_entry = builder.get_object("dataset_entry")
        self.alphabet_entry = builder.get_object("alphabet_entry")
        self.wordset_entry = builder.get_object("wordset_entry")
        self.charset_entry = builder.get_object("charset_entry")
        self.parse_entry = builder.get_object("parse_entry")
        self.dict_entry = builder.get_object("dict_entry")
        self.info_label = builder.get_object("info_label")

        self.info_label.configure(foreground="gray")

    def createparse(self):
        try:
            self.parser.parsefile("../datasets/" + self.dataset_entry.get(),
                                  "../charsets/" + self.charset_entry.get(),
                                  "../wordsets/" + self.wordset_entry.get(),
                                  "../parsed_datasets/" + self.parse_entry.get(),
                                  "../alphabets/" + self.alphabet_entry.get())

            info_text = "Dataset parsed in \" ../parsed_datasets/" + self.parse_entry.get()
            self.info_label.configure(text=info_text, foreground="green")
        except FileNotFoundError as f:
            info_text = "File \"" + f.filename + "\" not found"
            self.info_label.configure(text=info_text, foreground="red")

    def createdict(self):
        self.parser.createdict("../parsed_datasets/" + self.parse_entry.get(),
                               "../dictionaries/" + self.dict_entry.get())

    # def createcharset(self):
    #
    #
    # def createdict(self):


if __name__ == "__main__":
    root = tkinter.Tk()
    app = Application(root)
    root.mainloop()
