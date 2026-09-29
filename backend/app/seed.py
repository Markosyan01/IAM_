from .models import Course, Lesson

IMG = "https://images.unsplash.com/{}?auto=format&fit=crop&w=900&q=70"

# (slug, photo, level, title(en,ru,hy), desc(en,ru,hy), lessons[(title, body, code)])
DATA = [
 ("python", "photo-1515879218367-8466d910aaa4", "beginner",
  ("Python Basics", "Основы Python", "Python-ի հիմունքներ"),
  ("Variables, loops and functions from zero.", "Переменные, циклы и функции с нуля.", "Փոփոխականներ, ցիկլեր և ֆունկցիաներ զրոյից։"),
  [(("Variables and types", "Переменные и типы", "Փոփոխականներ և տիպեր"),
    ("A variable is a name for a value. Python figures out the type for you.", "Переменная — это имя для значения. Python сам определяет тип.", "Փոփոխականը արժեքի անուն է։ Python-ը տիպը որոշում է ինքնաբերաբար։"),
    'name = "Ani"\nage = 21\nprint(name, age, type(age))'),
   (("Loops", "Циклы", "Ցիկլեր"),
    ("Use a for loop to repeat an action for every item.", "Цикл for повторяет действие для каждого элемента.", "for ցիկլը կրկնում է գործողությունը յուրաքանչյուր տարրի համար։"),
    'for i in range(3):\n    print("Hello", i)')]),
 ("javascript", "photo-1461749280684-dccba630e2f6", "beginner",
  ("JavaScript Essentials", "Основы JavaScript", "JavaScript-ի հիմունքներ"),
  ("Make web pages interactive.", "Сделайте страницы интерактивными.", "Դարձրեք վեբ էջերը ինտերակտիվ։"),
  [(("Functions", "Функции", "Ֆունկցիաներ"),
    ("A function packages code you can run again and again.", "Функция объединяет код, который можно вызывать много раз.", "Ֆունկցիան կոդի մի հատված է, որը կարելի է կրկին ու կրկին կանչել։"),
    "const add = (a, b) => a + b;\nconsole.log(add(2, 3));"),
   (("The DOM", "DOM", "DOM"),
    ("The DOM lets JavaScript read and change the page.", "DOM позволяет JavaScript читать и менять страницу.", "DOM-ը թույլ է տալիս JavaScript-ին կարդալ և փոխել էջը։"),
    'document.querySelector("h1").textContent = "Hi!";')]),
 ("html-css", "photo-1498050108023-c5249f4df085", "beginner",
  ("HTML & CSS", "HTML и CSS", "HTML և CSS"),
  ("Build and style your first web page.", "Создайте и оформите первую веб-страницу.", "Ստեղծեք և ձևավորեք ձեր առաջին վեբ էջը։"),
  [(("Page structure", "Структура страницы", "Էջի կառուցվածքը"),
    ("Every page has a head and a body.", "У каждой страницы есть head и body.", "Յուրաքանչյուր էջ ունի head և body։"),
    "<html>\n  <head><title>Hello</title></head>\n  <body><h1>My page</h1></body>\n</html>"),
   (("Styling with CSS", "Оформление с CSS", "Ձևավորում CSS-ով"),
    ("CSS rules pick elements and set how they look.", "Правила CSS выбирают элементы и задают их вид.", "CSS կանոնները ընտրում են տարրերը և սահմանում դրանց տեսքը։"),
    "h1 {\n  color: #2f5bff;\n  font-size: 2rem;\n}")]),
 ("sql", "photo-1555066931-4365d14bab8c", "intermediate",
  ("SQL for Beginners", "SQL для начинающих", "SQL սկսնակների համար"),
  ("Query and shape data with MySQL.", "Запросы к данным в MySQL.", "Տվյալների հարցումներ MySQL-ում։"),
  [(("SELECT basics", "Основы SELECT", "SELECT-ի հիմունքներ"),
    ("SELECT reads rows from a table.", "SELECT читает строки из таблицы.", "SELECT-ը աղյուսակից կարդում է տողեր։"),
    "SELECT name, email FROM users;"),
   (("Filtering rows", "Фильтрация строк", "Տողերի զտում"),
    ("WHERE keeps only the rows that match a condition.", "WHERE оставляет только строки, подходящие под условие.", "WHERE-ը թողնում է միայն պայմանին համապատասխանող տողերը։"),
    "SELECT * FROM courses\nWHERE level = 'beginner';")]),
 ("react", "photo-1542831371-29b0f74f9713", "intermediate",
  ("React Fundamentals", "Основы React", "React-ի հիմունքներ"),
  ("Components, props and state.", "Компоненты, props и состояние.", "Կոմպոնենտներ, props և state։"),
  [(("Components", "Компоненты", "Կոմպոնենտներ"),
    ("A component is a function that returns UI.", "Компонент — это функция, возвращающая интерфейс.", "Կոմպոնենտը ֆունկցիա է, որը վերադարձնում է ինտերֆեյս։"),
    "function Hello({ name }) {\n  return <h1>Hello, {name}!</h1>;\n}"),
   (("State", "Состояние", "State (վիճակ)"),
    ("State remembers values between renders.", "Состояние хранит значения между отрисовками.", "State-ը հիշում է արժեքները վերարտապատկերումների միջև։"),
    "const [count, setCount] = useState(0);\n<button onClick={() => setCount(count + 1)}>{count}</button>")]),
 ("git", "photo-1517694712202-14dd9538aa97", "beginner",
  ("Git & GitHub", "Git и GitHub", "Git և GitHub"),
  ("Track changes and collaborate.", "Отслеживайте изменения и работайте в команде.", "Հետևեք փոփոխություններին և աշխատեք թիմով։"),
  [(("Your first commit", "Первый коммит", "Առաջին commit-ը"),
    ("A commit saves a snapshot of your work.", "Коммит сохраняет снимок вашей работы.", "Commit-ը պահպանում է ձեր աշխատանքի պատկերը։"),
    'git init\ngit add .\ngit commit -m "First commit"'),
   (("Branches", "Ветки", "Ճյուղեր"),
    ("Branches let you try ideas without breaking main.", "Ветки позволяют пробовать идеи, не ломая main.", "Ճյուղերը թույլ են տալիս փորձել գաղափարներ՝ առանց main-ը փչացնելու։"),
    "git switch -c my-idea\ngit push -u origin my-idea")]),
]


def seed(db):
    if db.query(Course).count():
        return
    for slug, photo, level, t, d, lessons in DATA:
        c = Course(slug=slug, image=IMG.format(photo), level=level,
                   title_en=t[0], title_ru=t[1], title_hy=t[2],
                   desc_en=d[0], desc_ru=d[1], desc_hy=d[2])
        for i, (lt, lb, code) in enumerate(lessons, 1):
            c.lessons.append(Lesson(position=i, code=code,
                title_en=lt[0], title_ru=lt[1], title_hy=lt[2],
                body_en=lb[0], body_ru=lb[1], body_hy=lb[2]))
        db.add(c)
    db.commit()
