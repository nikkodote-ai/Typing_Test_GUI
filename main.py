import time
import tkinter as tk

from word_bank import Wordbank

#-----CONSTANTS-----#
BG_COLOR = '#F8F0E3'
FONT = ('Lemon/Milk', 16)
ENTRY_FONT = ('Trebuchet MS Bold', 22)
TEXTBOX_FONT = ('Trebuchet MS Bold', 27)
TIMER_FONT = ('Hey August', 35)

#----WORDBANK----#
wordbank = Wordbank()

#----SWITCH------#
global continue_test
continue_test = True

#-----GUI-----#
class MainApplication(tk.Frame):
    def __init__(self, parent):
        self.timer = 60
        self.master_start = time.time()
        self.start = time.time()
        self.typing_time = 0
        self.gross_wpm = 0
        self.gross_cpm = 0

        tk.Frame.__init__(self, parent)

        parent.title('Typing Test version 1.0 ND')
        # make canvas
        self.canvas = tk.Canvas(self, width=800, height=600, background=BG_COLOR)
        self.canvas.grid(columnspan=7, rowspan=3, )

        # label for Metrics, all found in row 1
        tk.Label(self, text='Corrected CMP:', font=FONT, background=BG_COLOR).grid(row=0, column=0, padx=(30, 0))

        self.cpm = tk.Label(self, text='0', width=5, font=FONT, background=BG_COLOR, borderwidth=2, relief='solid')
        self.cpm.grid(row=0, column=1)

        tk.Label(self, text='WPM:', font=FONT, background=BG_COLOR).grid(row=0, column=2)

        self.wpm = tk.Label(self, text='0', font=FONT, width=4, background=BG_COLOR, borderwidth=2, relief='solid')
        self.wpm.grid(row=0, column=3)

        tk.Label(self, text='Time Left:', font=FONT, background=BG_COLOR).grid(row=0, column=4)

        # timer label
        self.timer_label = tk.Label(self, width=3, text=self.timer, font=TIMER_FONT, background=BG_COLOR, fg='#005c75')
        self.timer_label.grid(row=0, column=5)

        if continue_test:
            self.update_wpm()  # add this with timer
            self.update_timer()

        tk.Button(self, text='Restart', font=FONT, background=BG_COLOR, relief='flat', command=self.game_end).grid(
            row=0, column=6, padx=(0, 30))

        # make the Textbox widget
        self.textbox = tk.Text(self, height=6, width=30, font=TEXTBOX_FONT, background='white')
        self.textbox.grid(row=1, columnspan=7)

        # make the Entry box widget for touch typing
        self.user_entry = tk.Entry(self, relief='flat', width=25, font=ENTRY_FONT, justify='center')
        self.user_entry.grid(columnspan=7, row=2)
        self.user_entry.bind('<space>', self.submit)
        self.user_entry.focus_set()
        # self.user_entry.bind('<Return>', self.game_end)
        self.textbox.after(500, self.textbox.config(background='white'))
        self.update_display()

    def update_display(self):
        first_30_words = wordbank.all_english_words[:33]
        display_text = '   '.join(first_30_words)
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, display_text)

    def update_wpm(self):

        if self.typing_time != 0:
            corrected_list = list(set(wordbank.attempted).intersection(set(wordbank.submitted_words)))
            len_chars = ''.join(corrected_list)
            self.final_corrected_cpm = round(((len(len_chars)) / self.typing_time) * 60)
            self.wpm.config(text=self.final_corrected_cpm / 5)
            self.cpm.config(text=self.final_corrected_cpm)
        else:
            self.final_corrected_cpm = 0

    def update_timer(self):
        # subtract 1 second every second
        self.update_wpm()
        if self.timer < 1:
            self.game_end()
        else:
            if continue_test:
                self.timer -= 1
                self.timer_label.config(text=self.timer)
                self.timer_label.after(1000, self.update_timer)

    def submit(self, key_pressed):
        self.stop = time.time()
        self.typing_time = self.stop - self.start
        print(self.typing_time)
        current_word = wordbank.all_english_words[0]
        typed_word = self.user_entry.get().strip()
        self.user_entry.delete(0, tk.END)
        if typed_word == current_word:
            self.textbox.config(background='#c7ffbf')
            wordbank.correct_counter += 1
            # print(f'CORRECT: typed word = "{typed_word}", current word: "{current_word}"')
        else:
            self.textbox.config(background='#ffbfbf')
            wordbank.mistake_counter += 1
            # print(f'MISTAKE: typed word = "{typed_word}", current word: "{current_word}"')

        self.attempted_words = wordbank.all_english_words.pop(0)
        wordbank.attempted.append(self.attempted_words)
        wordbank.submitted_words.append(typed_word)
        wordbank.total_submission += 1
        # print(f'submitted: {wordbank.submitted_words} correct: {wordbank.correct_counter}')
        # print(f'attempted: {wordbank.attempted}, mistakes: {wordbank.mistake_counter}')
        self.update_display()

    def game_end(self, *enter_key):
        """End the game and break down the score"""
        # finalization of metrics

        self.total_chars_typed = ''.join(wordbank.submitted_words)
        self.gross_wpm = round(((len(self.total_chars_typed) / 5) / self.typing_time) * 60, 2)
        self.gross_cpm = round(((len(self.total_chars_typed)) / self.typing_time) * 60)

        # switch off
        global keep_running
        keep_running = False

        self.timer_label.config(text=self.timer)
        self.wpm.config(text='DONE')
        self.user_entry.config(text='')
        self.popup = tk.Toplevel(background=BG_COLOR)
        self.popup.title("Time is up")

        pop_can = tk.Canvas(self.popup, background=BG_COLOR)
        pop_can.grid(columnspan=3, row=2)

        final_texts = f'In reality, you typed {self.gross_cpm} CPM,' \
                      f' but you made {wordbank.mistake_counter} mistakes ' \
                      f'(out of {wordbank.total_submission} words), which ' \
                      f'were not counted in the corrected scores.'

        tk.Label(self.popup, text='Your score:', font=ENTRY_FONT, background=BG_COLOR).grid(row=0, column=0)
        tk.Label(self.popup, text=self.final_corrected_cpm, width=4, font=('Hey August', 36), fg='red',
                 background=BG_COLOR).grid(row=0, column=1)
        tk.Label(self.popup, text='CPM', font=ENTRY_FONT, background=BG_COLOR).grid(row=0, column=2, )
        tk.Label(self.popup, text='that is:', font=ENTRY_FONT, background=BG_COLOR).grid(row=1, column=0)
        tk.Label(self.popup, text=self.final_corrected_cpm / 5, width=4, font=('Hey August', 25),
                 background=BG_COLOR).grid(row=1, column=1)
        tk.Label(self.popup, text='WPM', font=ENTRY_FONT, background=BG_COLOR).grid(row=1, column=2)

        # final word. full disclosure of total and mistakes
        unofficial_results = tk.Text(self.popup, font=('Hunting', 30), width=23, height=7, wrap=tk.WORD, fg='#191d1f',
                                     relief='flat', background=BG_COLOR)
        unofficial_results.grid(row=2, column=0, columnspan=3)

        # add centered text
        unofficial_results.tag_configure("center", justify='center')
        unofficial_results.insert(tk.END, final_texts)
        unofficial_results.tag_add("center", "1.0", "end")

        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.popup.destroy()
        self.destroy()
        self.quit()


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).grid()
    root.mainloop()
    print('Type test done. Thank you for your patronage')
