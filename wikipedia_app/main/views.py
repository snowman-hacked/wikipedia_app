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
            # 모호한 결과일 경우 선택지 제공
            return render(request, "main/index.html", {"options": e.options, "search": search})

        except PageError:
            return render(request, "main/index.html", {"error": "검색 결과를 찾을 수 없습니다.", "search": search})
        
        except Exception as e:
            return render(request, "main/index.html", {"error": str(e), "search": search})

    return render(request, "main/index.html")
