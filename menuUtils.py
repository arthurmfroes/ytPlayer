import curses
import sys
import pyperclip
from ytPlayerUtils import YouTubePlayer


def draw_main_menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.refresh()
    stdscr_height, stdscr_width = stdscr.getmaxyx()

    title = "Menu Principal"
    options = ["Inserir Playlist", "Ver Playlists", "Sair"]
    selected_option = 0

    title_y = stdscr_height // 2 - len(options) // 2 - 2
    title_x = stdscr_width // 2 - len(title) // 2 - 1
    option_y = title_y + 2
    option_x = stdscr_width // 2 - 10

    stdscr.addstr(title_y, title_x, title, curses.A_BOLD)

    for i, option in enumerate(options):
        if i == selected_option:
            attr = curses.A_BOLD | curses.color_pair(2)
        else:
            attr = curses.color_pair(1)
        stdscr.addstr(option_y + i, option_x, f"{option:^18}", attr)

    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_option == 0:
                return draw_playlist_insert_menu(stdscr)  # Chamando a função draw_playlist_insert_menu

            elif selected_option == 1:
                # Implementar a lógica para "Ver Playlists"
                break
            elif selected_option == 2:
                sys.exit()

        stdscr.clear()
        stdscr.addstr(title_y, title_x, title, curses.A_BOLD)
        for i, option in enumerate(options):
            if i == selected_option:
                attr = curses.A_BOLD | curses.color_pair(2)
            else:
                attr = curses.color_pair(1)
            stdscr.addstr(option_y + i, option_x, f"{option:^18}", attr)
        stdscr.refresh()

def draw_playlist_insert_menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.refresh()
    stdscr_height, stdscr_width = stdscr.getmaxyx()

    title = "Inserir Playlist"
    instruction = "Cole o link da playlist e pressione Enter:"
    link_box_height = 3
    link_box_width = 60
    link_box_y = stdscr_height // 2 - link_box_height // 2
    link_box_x = stdscr_width // 2 - link_box_width // 2

    quit_button_text = "Pressione Backspace para sair"
    quit_button_y = link_box_y + link_box_height + 1
    quit_button_x = stdscr_width // 2 - len(quit_button_text) // 2

    stdscr.addstr(stdscr_height // 2 - 5, stdscr_width // 2 - len(title) // 2, title, curses.A_BOLD)
    stdscr.addstr(stdscr_height // 2 - 3, stdscr_width // 2 - len(instruction) // 2, instruction, curses.A_NORMAL)

    link_text = ""
    link_text_x = link_box_x + 1
    link_text_y = link_box_y + 1
    while True:
        stdscr.clear()
        stdscr.bkgd(' ', curses.color_pair(1))
        stdscr.refresh()

        max_display_length = link_box_width - 5
        for i in range(len(link_text)):
            if i >= max_display_length:
                pontos = "..."
                stdscr.addstr(link_text_y, link_text_x + i, pontos, curses.A_NORMAL)
                break
            stdscr.addch(link_text_y, link_text_x + i, link_text[i], curses.A_NORMAL)

        stdscr.addstr(quit_button_y, quit_button_x, quit_button_text, curses.A_BOLD)

        stdscr.addstr(stdscr_height // 2 - 5, stdscr_width // 2 - len(title) // 2, title, curses.A_BOLD)
        stdscr.addstr(stdscr_height // 2 - 3, stdscr_width // 2 - len(instruction) // 2, instruction, curses.A_NORMAL)

        for i in range(link_box_width):
            stdscr.addch(link_box_y, link_box_x + i, curses.ACS_HLINE)
            stdscr.addch(link_box_y + 2, link_box_x + i, curses.ACS_HLINE)
        stdscr.addch(link_box_y, link_box_x, curses.ACS_ULCORNER)
        stdscr.addch(link_box_y, link_box_x + link_box_width - 1, curses.ACS_URCORNER)
        stdscr.addch(link_box_y + 1, link_box_x, curses.ACS_VLINE)
        stdscr.addch(link_box_y + 1, link_box_x + link_box_width - 1, curses.ACS_VLINE)
        stdscr.addch(link_box_y + 2, link_box_x, curses.ACS_LLCORNER)
        stdscr.addch(link_box_y + 2, link_box_x + link_box_width - 1, curses.ACS_LRCORNER)

        curses.flushinp()
        key = stdscr.getch()
        if key == 22:
            link_text = pyperclip.paste()
        elif key == 127 or key == curses.KEY_BACKSPACE or key == 263:
            return
        elif key == 10:
            if link_text == "":
                continue
            else:
                return draw_playlist_access_menu(stdscr, link_text)
            
def draw_playlist_access_menu(stdscr, playlist_url):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.refresh()
    stdscr_height, stdscr_width = stdscr.getmaxyx()

    title = "Playlist"
    loading_text = "Carregando playlist..."
    error_text = "Erro ao acessar a playlist!"
    instructions_text = "Pressione Backspace para sair"
    success_text = "Playlist encontrada!"

    stdscr.addstr(stdscr_height // 2 - 3, stdscr_width // 2 - len(title) // 2, title, curses.A_BOLD)
    stdscr.addstr(stdscr_height // 2 - 1, stdscr_width // 2 - len(loading_text) // 2, loading_text)
    stdscr.refresh()

    try: 
        playlist = YouTubePlayer.retrieve_all_playlist_videos(playlist_url)
        playlist_items = [video['title'] for video in playlist[1:]]  # Ignora o primeiro elemento (informações da playlist)

        # Definir a opção inicialmente selecionada como a primeira da lista
        selected_option = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Escolha uma música da playlist:", curses.A_BOLD)

            # Desenha as opções da playlist
            for i, item in enumerate(playlist_items):
                if i == selected_option:
                    stdscr.addstr(i + 2, 2, f"> {item}", curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 2, f"  {item}", curses.color_pair(1))

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(playlist_items)
            elif key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(playlist_items)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                try:
                    YouTubePlayer.startPlayer(playlist[selected_option + 1]['link'])  # Ignora o primeiro elemento (informações da playlist)
                    stdscr.getch()
                except Exception as e:
                    # Limpa a tela e exibe a mensagem de erro
                    stdscr.clear()
                    stdscr.addstr(stdscr_height // 2 - 1, stdscr_width // 2 - len(str(e)) // 2, str(e), curses.color_pair(2))
                    stdscr.addstr(stdscr_height // 2 + 2, stdscr_width // 2 - len(instructions_text)// 2, instructions_text, curses.color_pair(1))
                    stdscr.refresh()
                    # Aguarda uma ação do usuário
                    while True:
                        key = stdscr.getch()
                        if key == 127 or key == curses.KEY_BACKSPACE or key == 263:
                            return draw_main_menu(stdscr)
    except Exception as e:
        # Limpa a tela e exibe a mensagem de erro
        stdscr.clear()
        stdscr.addstr(stdscr_height // 2 - 1, stdscr_width // 2 - len(str(e)) // 2, str(e), curses.color_pair(2))
        stdscr.addstr(stdscr_height // 2 + 2, stdscr_width // 2 - len(instructions_text)// 2, instructions_text, curses.color_pair(1))
        stdscr.refresh()
        # Aguarda uma ação do usuário
        while True:
            key = stdscr.getch()
            if key == 127 or key == curses.KEY_BACKSPACE or key == 263:
                return draw_main_menu(stdscr)


    
def main(stdscr):
    args = None
    while True:
        draw_func = draw_main_menu
        if args is not None:
            draw_func, args = draw_func(stdscr, args)  # Agora estamos chamando draw_func com stdscr e args
        else:
            draw_func = draw_func(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
