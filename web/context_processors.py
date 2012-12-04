def view_name_context_processor(request):
    return {
        'view_name': request.view_name,
    }