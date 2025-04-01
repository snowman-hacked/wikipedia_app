# 위키백과 검색 웹앱 (Wikipedia Search App with Django)

이 프로젝트는 Django와 `wikipedia` 라이브러리를 활용하여 만든 간단한 위키백과 검색 웹앱입니다. 사용자가 검색어를 입력하면 위키백과의 요약 정보를 제공하며, 모호한 검색어(예: "Apple")의 경우 선택지를 제시해 정확한 검색을 유도합니다.

---

## 주요 기능

- 위키백과 검색 및 요약 결과 제공 (3문장)
- 모호한 검색어 입력 시 선택지 제공 (`DisambiguationError` 대응)

---

## 프로젝트 구조

```
wikipedia_app/
├── db.sqlite3
├── manage.py
├── main/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── templates/
│   │   └── main/
│   │       └── index.html
│   ├── tests.py
│   ├── urls.py
│   ├── views.py  ← 핵심 로직 구현 파일
│   └── __init__.py
├── wikipedia_app/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
```

---

## 설치 및 실행 방법

### 1. 프로젝트 클론

```bash
git clone https://github.com/snowman-hacked/wikipedia_app.git
cd wikipedia-django-app
```

### 2. 가상환경 생성(선택사항)

```bash
python -m venv venv
source env/bin/activate
```

### 3. 필요한 라이브러리 설치

```bash
pip install django wikipedia
```

### 4. 마이그레이션 적용

```bash
python manage.py migrate
```

### 5. 서버 실행

```bash
python manage.py runserver 0.0.0.0:8000
```

이후 브라우저에서 [http://localhost:8000](http://localhost:8000) 접속

---

## 사용 방법

1. 검색어 입력 (예: "Python")
2. 검색 결과가 1개일 경우 요약 정보 출력
3. 모호한 단어(예: "Mercury") 입력 시, 선택지 목록이 버튼으로 표시됨 → 클릭 시 재검색 진행

---

## 주요 코드

### `views.py`

```python
from django.shortcuts import render
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

def home(request): 
    if request.method == "POST": 
        search = request.POST['search'] 
        try: 
            result = wikipedia.summary(search, sentences=3)
            return render(request, "main/index.html", {"result": result, "search": search})
        
        except DisambiguationError as e:
            return render(request, "main/index.html", {"options": e.options, "search": search})

        except PageError:
            return render(request, "main/index.html", {"error": "검색 결과를 찾을 수 없습니다.", "search": search})

        except Exception as e:
            return render(request, "main/index.html", {"error": str(e), "search": search})

    return render(request, "main/index.html")
```

---

### `index.html`

```html
<form method="post">
    {% csrf_token %}
    <input type="text" name="search" placeholder="위키백과 검색" value="{{ search }}">
    <button type="submit">검색</button>
</form>

{% if result %}
    <h2>"{{ search }}"에 대한 요약</h2>
    <p>{{ result }}</p>
{% endif %}

{% if options %}
    <h3>"{{ search }}"은(는) 여러 의미를 가질 수 있습니다. 아래에서 선택해주세요:</h3>
    <ul>
        {% for option in options %}
            <li>
                <form method="post" style="display:inline;">
                    {% csrf_token %}
                    <input type="hidden" name="search" value="{{ option }}">
                    <button type="submit">{{ option }}</button>
                </form>
            </li>
        {% endfor %}
    </ul>
{% endif %}

{% if error %}
    <p style="color:red;">{{ error }}</p>
{% endif %}
```

---

## 참고 자료

- 본 프로젝트는 [GeeksforGeeks의 예제](https://www.geeksforgeeks.org/wikipedia-search-app-project-using-django/)를 기반으로 하였으며, `DisambiguationError`에 대한 사용자 인터랙션 기능을 추가하였습니다.
- Wikipedia API는 [`wikipedia` 라이브러리](https://pypi.org/project/wikipedia/)를 사용합니다.
