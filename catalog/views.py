from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
    num_books = Book.objects.all().count()

    num_instances = BookInstance.objects.all().count()

    num_num_instance_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()
    

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request, 'index.html', context={'num_books': num_books, 'num_instances': num_instances, 'num_num_instance_available': num_num_instance_available, 'num_authors': num_authors, 'num_visits': num_visits}
    )

class BookListView(generic.ListView):
    model = Book

    context_object_name = 'my_book_list'

    template_name = 'catalog/book_list.html'

    

    def get_queryset(self):
        return Book.objects.all()[:5] # Получить 5 книг, содержащих 'war' в заголовке
    
    def get_context_data(self, **kwargs):
        context =  super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'какие то непонятные данные'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    





