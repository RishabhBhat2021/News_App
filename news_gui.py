import news_data as nd

import tkinter as tk
from tkinter import ttk

LARGE_FONT_BOLD = ("Helvetica", 25, 'bold')
MEDIUM_FONT_BOLD = ("Helvetica", 13, 'bold')
MEDIUM_FONT = ("Helvetica", 13)


class NewsApp(tk.Tk):
    def __init__(self, *args, **kwargs):       
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.title(self, "News")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, DetailPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


class StartPage(tk.Frame, nd.NewsData, nd.NewsDetail):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        nd.NewsData.__init__(self)

        self.news_articles = nd.NewsData.get_headlines(self)

        self.controller = controller

        heading = tk.Label(self, text="TOP HEADLINES", font=LARGE_FONT_BOLD)
        heading.pack(side="top")

        quit_button = ttk.Button(self, text="Quit", command=quit)
        quit_button.pack(side="top")

        self.headline_display = tk.Listbox(self, width=130, height=40, font=MEDIUM_FONT_BOLD)
        self.headline_display.pack(fill="both", expand=True, side=tk.LEFT)

        for article in self.news_articles:
            self.headline_display.insert(tk.END, article)
            self.headline_display.insert(tk.END, "")

        self.headline_display.bind("<Double-Button-1>", self.get_selected_headline)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.headline_display.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.headline_display.yview)

        self.headline_var = tk.StringVar()

    def get_selected_headline(self, event):
        self.detail_page_object = self.controller.get_page(DetailPage)

        widget = event.widget
        selection = widget.curselection()
        self.selected_headline = widget.get(selection[0])

        article_link = nd.NewsData.get_link(self, self.selected_headline)

        if self.selected_headline != "":
            nd.NewsDetail.__init__(self, article_link)

            self.detail_page_object.news_detail_display.delete(1.0, tk.END)
            self.detail_page_object.news_detail_display.insert(tk.END, nd.NewsDetail.get_sub_heading(self) + "\n")
            self.detail_page_object.news_detail_display.insert(tk.END, nd.NewsDetail.get_paragraphs(self) + "\n")

            self.headline_var.set(nd.NewsDetail.get_main_heading(self))

            self.controller.show_frame(DetailPage)


class DetailPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        start_page_object = self.controller.get_page(StartPage)

        headline_label = tk.Label(self, textvariable=start_page_object.headline_var, font=MEDIUM_FONT_BOLD)
        headline_label.pack(side="top")

        home_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame(StartPage))
        home_button.pack(side="top")

        self.news_detail_display = tk.Text(self, width=130, height=40, font=MEDIUM_FONT)
        self.news_detail_display.pack(fill="both", expand=True, side=tk.LEFT)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.news_detail_display.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.news_detail_display.yview)
