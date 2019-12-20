from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from memes.forms import MemForm
from memes.models import Mem, Movie


class ListMems(View):
    def get(self, request):
        mems = Mem.objects.all().order_by('-created_at')

        paginator = Paginator(mems, 6)
        page = int(request.GET.get('page', 1))

        if page > 1:
            return render(
                request,
                'memes/includes/mems.html',
                context={
                    'mems': paginator.get_page(page)
                }
            )

        return render(
            request,
            'memes/index.html',
            context={
                'mems': paginator.get_page(page),
                'pages': paginator.num_pages
            }
        )


class ListMovies(View):
    def get(self, request):
        movies = Movie.objects.all().order_by('-created_at')

        paginator = Paginator(movies, 10)
        page = int(request.GET.get('page', 1))

        if page > 1:
            return render(
                request,
                'memes/includes/movies.html',
                context={
                    'movies': paginator.get_page(page)
                }
            )

        return render(
            request,
            'memes/movies.html',
            context={
                'movies': paginator.get_page(page),
                'pages': paginator.num_pages
            }
        )


class ViewMem(View):
    def get(self, request, slug):
        mem = get_object_or_404(Mem, slug=slug)

        return render(
            request,
            'memes/mem.html',
            context={
                'mem': mem
            }
        )


class CreateMem(View):
    def get(self, request):
        form = MemForm()

        return render(
            request,
            'memes/create_mem.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        form = MemForm(request.POST, request.FILES)

        if form.is_valid():
            mem = form.save()
            mem.save()

            return redirect(mem)

        return render(
            request,
            'memes/create_mem.html',
            context={
                'form': form
            }
        )
