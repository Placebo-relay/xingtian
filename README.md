# xingtian demo project + radio script via vlc
pygame pywin32 screeninfo python-vlc test

Learned:
1. collect monitor data (screeninfo)
2. how to create a desktop mascot in a no_frame floating mode on the desktop screen transparent layer (pywin32)
4. streaming (python-vlc)

made during university algorithms&alg.languages

## ru:

### (Esc)ape Xingtian = мини-игра с радио для
* тестирования знания тонов китайского (изначально создавался без pywin32)
* можно использовать как маскота (скопировать часть кода с pywin32/screeninfo и сделать своего персонажа, анимировать спрайты)
* режимы: радио, тона, радио+тона(хардкор)
* нулевая помощь пользователю (суть игры = выйти из игры, либо зная клавишу выхода, либо пройдя тоны)
* кринжовые монстры вылезают при неверно угаданных тонах

### планы

* планируется отключить выход по клавише и закронить, выход = правильно назвать тона
* планируется добавить-анимировать спрайты
* планируется рефакторинг под ООП подход, замаксить читабельность
