import json
from pathlib import Path
import sys
from .engine import suite,run_trial,minimize
ROOT=Path(__file__).resolve().parent
MESSAGES={"fr":{"help":"Utilisation : python -m brain_breakers demo|suite [--backends sqlite_fts5,chroma,qdrant_local]|trial cas.json|minimize cas.json|serve [port] [--lang fr|en|es]","error":"Entrée non valide ou moteur absent","ready":"Laboratoire mémoire local"},"en":{"help":"Usage: python -m brain_breakers demo|suite [--backends sqlite_fts5,chroma,qdrant_local]|trial case.json|minimize case.json|serve [port] [--lang fr|en|es]","error":"Invalid input or missing engine","ready":"Local memory laboratory"},"es":{"help":"Uso: python -m brain_breakers demo|suite [--backends sqlite_fts5,chroma,qdrant_local]|trial caso.json|minimize caso.json|serve [puerto] [--lang fr|en|es]","error":"Entrada no válida o motor ausente","ready":"Laboratorio de memoria local"}}
def examples():return json.loads((ROOT/'examples/cases.json').read_text())
def main(argv=None):
    args=list(sys.argv[1:] if argv is None else argv);lang='en';backends=['sqlite_fts5']
    try:
        if '--lang' in args:i=args.index('--lang');lang=args[i+1];del args[i:i+2]
        if '--backends' in args:i=args.index('--backends');backends=args[i+1].split(',');del args[i:i+2]
        if lang not in MESSAGES:raise ValueError('language')
        if not args or args[0] in ('help','--help'):print(MESSAGES[lang]['help']);return 0
        cmd=args.pop(0)
        if cmd=='serve':
            from .server import serve
            port=int(args[0]) if args else 8772;print(f'{MESSAGES[lang]["ready"]}: http://127.0.0.1:{port}/?lang={lang}',flush=True);serve(port);return 0
        if cmd in ('demo','suite'):result=suite(examples(),backends)
        elif cmd=='trial':
            case=json.loads(Path(args[0]).read_text());result=run_trial(case,backends[0],case.get('injected_fault','none'))
        elif cmd=='minimize':
            case=json.loads(Path(args[0]).read_text());result=minimize(case,backends[0],case.get('injected_fault','none'))
        else:raise ValueError('command')
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ValueError,TypeError,KeyError,IndexError,OSError,ImportError):print(json.dumps({'error':'invalid_input','message':MESSAGES.get(lang,MESSAGES['en'])['error']}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
