function! ale_linters#amnd#amnd#Handle(buffer, lines) abort
    " Error format: <filename>:<lnum>:<col>: <text>
    " Error format: <filename>:<lnum>:<col>: error: <text>
    " Warning format: <filename>:<lnum>:<col>: warning: <text>
    let l:re = '\v(.+):([0-9]+):([0-9]+):\s+(warning:)?\s*(.+)\s*'
    let l:output = []

    for l:match in ale#util#GetMatches(a:lines, l:re)
        let l:cur_file = ale#path#Simplify(expand('#' . a:buffer . ':p'))
        let l:item = {
        \   'bufnr': a:buffer,
        \   'filename': l:match[1],
        \   'lnum': str2nr(l:match[2]),
        \   'col': str2nr(l:match[3]),
        \   'type': l:match[4] is# 'warning:' ? 'W' : 'E',
        \   'text': l:match[5],
        \}
        let l:error_file = ale#path#Simplify(l:item.filename)

        " The AMND compiler will also print warnings of included files
        " Thats the reason why all lines that doesn't have a matching
        " filename will be skipped. The cur_file and error_file are
        " simplified and should always be equal if the files are in the
        " same folder.
        if l:cur_file == l:error_file
            call add(l:output, l:item)
        endif
    endfor

    return l:output
endfunction



call ale#linter#Define('amnd', {
\   'name': 'amnd',
\   'executable': '/home/marco/workspace/Mindustry/AdvancedMindustryLogic/main.py',
\   'command': '/home/marco/workspace/Mindustry/AdvancedMindustryLogic/main.py %s --lint',
\   'callback': 'ale_linters#amnd#amnd#Handle',
\   'output_stream': 'stdout',
\})
