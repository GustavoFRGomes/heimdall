set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim

filetype plugin on
set tags=~/.vim/ctags,tags,.tags,../tags
map <C-;> :!ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .<CR><CR>


call vundle#begin()
"autocmd QuickFixCmdPost [^l]* nested lwindow
"set errorformat^=%-G%f:%l:\ warning:%m
"PLUGINS
Plugin 'gmarik/Vundle.vim'
Plugin 'tpope/vim-fugitive'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-commentary'
Plugin 'bling/vim-airline'
Plugin 'L9'
Plugin 'mattn/emmet-vim'
Plugin 'xuhdev/vim-latex-live-preview'
Plugin 'imain/notmuch-vim'
" Plugin 'indexer'

" Elixir
" Plugin 'huffman/vim-elixir'
" Plugin 'awetzel/elixir.nvim'
Plugin 'elixir-lang/vim-elixir'

Plugin 'vim-scripts/OmniCppComplete'
Plugin 'vim-scripts/DfrankUtil'
Plugin 'vim-scripts/vimprj'

Plugin 'jeffkreeftmeijer/vim-numbertoggle'

"Plugin 'ardagnir/vimbed' "needed for vimbed
"BUNDLES
" Bundle "aperezdc/vim-template"
Bundle "MarcWeber/vim-addon-mw-utils"
" Bundle "tomtom/tlib_vim"
" Bundle "honza/vim-snippets"
Bundle 'freeo/vim-kalisi'
Bundle 'altercation/vim-colors-solarized'
Bundle 'sickill/vim-monokai'
Bundle 'sfsekaran/cobalt.vim'
Bundle 'tomasr/molokai'

" My Themes
Plugin 'Valloric/vim-valloric-colorscheme'
Plugin 'wellsjo/wellsokai.vim'
Plugin 'fcevado/molokai_dark'
Plugin 'zsoltf/vim-maui'
Plugin 'bruschill/madeofcode'
Bundle 'Elle518/Duna'
Bundle 'petelewis/vim-evolution'
Bundle 'joshdick/onedark.vim'
Bundle 'Haron-Prime/Antares'
Bundle 'hewo/vim-colorscheme-deepsea'
Bundle 'christophermca/meta5'
Bundle 'ratazzi/blackboard.vim'
Bundle 'nielsmadan/harlequin'
Bundle 'sjl/badwolf'
Bundle 'vim-scripts/summerfruit256.vim'
Bundle 'flazz/vim-colorschemes'
Bundle 'trusktr/seti.vim'
Bundle 'znake/znake-vim'
Bundle 'stephanedemotte/beekai'
Bundle 'widatama/vim-phoenix'
" Bundle 'AlexMax/.vim'
Bundle 'vim-scripts/vibrantink'
Bundle 'gryftir/gryffin'
"
Plugin 'octol/vim-cpp-enhanced-highlight'
Plugin 'GertjanReynaert/cobalt2-vim-theme'
Plugin 'kien/ctrlp.vim'

"
call vundle#end()            " required
filetype plugin indent on    " required
set encoding=utf-8
set t_Co=256



" OmniCppComplete
let OmniCpp_ShowPrototypeInAbbr = 1 " show function parameters
let OmniCpp_NamespaceSearch = 1
let OmniCpp_GlobalScopeSearch = 1
let OmniCpp_ShowAccess = 1
let OmniCpp_MayCompleteDot = 1
let OmniCpp_MayCompleteArrow = 1
let OmniCpp_MayCompleteScope = 1
let OmniCpp_DefaultNamespaces = ["std", "_GLIBCXX_STD"]
" automatically open and close the popup menu / preview window
au CursorMovedI,InsertLeave * if pumvisible() == 0|silent! pclose|endif
set completeopt=menuone,menu,longest

syntax on
set hlsearch
set autoindent
set cindent
set tabstop=4
set shiftwidth=4
"set cursorcolumn
imap jk <Esc>
set nowrap
set nu
"
" colorscheme seti
" colorscheme kalisi
" colorscheme solarized
" colorscheme valloric
colorscheme 256-grayvim
" colorscheme molokai_dark
" set background=dark


hi CursorLine term=bold cterm=bold ctermbg=Black
set cursorline
set ruler
set guioptions-=r
set guioptions-=m
set guioptions-=T
imap <C-t> <Esc>:tabnew<cr>a
"imap <C-Space> <C-X><C-N>
nmap <C-t> :tabnew<cr>
"set rtp+=/usr/local/lib/python2.7/dist-packages/powerline/bindings/vim/
set laststatus=2

" let &t_AB="\e[48;5;%dm"
" let &t_AF="\e[38;5;%dm"
"command E Explore
" let g:notmuch_folders = [
" 	\ [ 'new', 'tag:inbox and tag:unread' ],
" 	\ [ 'inbox', 'tag:inbox' ],
" 	\ [ 'unread', 'tag:unread' ]
" 	\ ]
"let g:notmuch_reader = 'mutt -f %s'
" let g:notmuch_sendmail = 'sendmail'
" helptags ~/.vim/doc
" function MailFunc()
" 	execute ":silent !offlineimap && notmuch new"
	" redraw!
	" NotMuch
	" colorscheme kalisi
	" redraw!
" endfunction

" command Mail exec MailFunc()

"inoremap <expr> j pumvisible() ? "\<C-N>" : "j"
"inoremap <expr> k pumvisible() ? "\<C-P>" : "k"
"Disable arrow keys
inoremap  <Up>     <NOP>
inoremap  <Down>   <NOP>
inoremap  <Left>   <NOP>
inoremap  <Right>  <NOP>
noremap   <Up>     <NOP>
noremap   <Down>   <NOP>
noremap   <Left>   <NOP>
noremap   <Right>  <NOP>

set wildignore+=*/.git/*,*/node_modules/*,*/.svn/*,*/*.o
"au BufWinEnter * let w:m1=matchadd('Search', '\%<81v.\%>77v', -1)
"au BufWinEnter * let w:m2=matchadd('ErrorMsg', '\%>80v.\+', -1)
set colorcolumn=80
" making the 80 char stick to some files
au BufRead,BufNewFile *.md setlocal textwidth=80
au BufRead,BufNewFile *.py setlocal textwidth=80
au BufRead,BufNewFile *.cpp setlocal textwidth=80
au BufRead,BufNewFile *.c setlocal textwidth=80
au BufRead,BufNewFile *.tex setlocal textwidth=80

" if !exists('g:airline_symbols')
" 	let g:airline_symbols = {}
" endif
if !exists('g:airline_symbols')
	let g:airline_symbols = {}
endif
let g:airline_left_sep = ''
let g:airline_left_alt_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#whitespace#mixed_indent_algo = 1
let g:airline#extensions#tabline#left_sep = ''
let g:airline#extensions#tabline#left_alt_sep = '|'
let g:airline_powerline_fonts=1

let g:airline_symbols.branch = ''
let g:airline_symbols.readonly = ''
let g:airline_symbols.linenr = ''
" let g:airline_left_sep = ' '
" let g:airline_left_alt_sep = ' '
" let g:airline_right_sep = ' '
" let g:airline_right_alt_sep = ' '
" let g:airline#extensions#tabline#enabled = 1
" let g:airline#extensions#tabline#left_sep = ' '
" let g:airline#extensions#tabline#left_alt_sep = '|'

set noshowmode
" let g:airline_theme = 'badwolf'
let g:airline_theme = 'serene'

map <C-j> <C-W>+
map <C-k> <C-W>-
map <C-l> <C-W>>
map <C-h> <C-W><

let g:tex_flavor='latex'
let g:livepreview_previewer = 'evince'

" set fillchars=""
