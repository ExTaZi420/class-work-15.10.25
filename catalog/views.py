from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin


@login_required
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
    

# def books(request):
#     num_visits_book = request.session.get('num_visits_book', 0)
#     request.session['num_visits_book'] = num_visits_book+1
#     return render(
#         request, "book_list.html",
#           context={'num_visits_book':num_visits_book,})



# def sessionForBook(request):
#     count_visit = request.session.get('count_visit', 0)
#     request.session['count_visit'] = count_visit+1
#     return render(request, 'book_list.html', context={'count_visit':count_visit})


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})



class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/borrowed_books.html'
    context_object_name = 'borrowed_books'
    
    def get_queryset(self):
        return BookInstance.objects.filter(status='o').order_by('due_back')




