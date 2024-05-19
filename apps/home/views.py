from django import template
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

# Import helper functions
from staticfiles.helpers.helpers import *
from staticfiles.model_trainer import model_trainer_controller
from staticfiles.scraping_service_installer import installer_controller

system = platform.system()


def predict(request):
    context = {
        'segment': 'predict',
        'database_stats': get_database_stats(),
    }

    html_template = loader.get_template('home/predict.html')
    return HttpResponse(html_template.render(context, request))


@csrf_exempt
@require_POST
def predict_price(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data['offer_type'][0] == 1:
                # Prenájom
                predicted_price = load_model_and_predict(data, 'Prenájom')[0]
            else:
                # Predaj
                predicted_price = load_model_and_predict(data, 'Predaj')[0]
            return JsonResponse({'predicted_price': predicted_price})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def average_price(request):
    context = {
        'segment': 'average_price',
        'database_stats': get_database_stats(),
    }

    html_template = loader.get_template('home/property_price.html')
    return HttpResponse(html_template.render(context, request))


def interactive_map(request):
    context = {
        'segment': 'interactive_map',
        'database_stats': get_database_stats(),
    }

    html_template = loader.get_template('home/interactive_map.html')
    return HttpResponse(html_template.render(context, request))


def data_analysis(request):
    context = {
        'segment': 'data_analysis',
    }

    html_template = loader.get_template('home/data_analysis.html')
    return HttpResponse(html_template.render(context, request))


@csrf_exempt
@require_POST
def get_diagram_values(request):
    try:
        data = json.loads(request.body)
        sql_query = data.get('sql_query')
        print(sql_query)

        if not sql_query:
            return JsonResponse({'error': 'No SQL query provided'}, status=400)

        results = execute_sql_query(sql_query)

        if results is None:
            return JsonResponse({'error': 'Failed to execute query or no data found.'}, status=404)

        return JsonResponse({'diagram_values': results}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        print(f'Error retrieving diagram data: {e}')
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


async def settings(request):
    # Scraping version
    scraping_service_v = scraping_service_version()
    scraping_service_v = scraping_service_v.lower() if 'error' not in scraping_service_v else 'VERSION ERROR'

    # Scraping interval
    scraping_service_int = scraping_service_scrape_interval()
    scraping_service_int = scraping_service_int[
        'scraping_service_interval'] if 'error' not in scraping_service_int else 'LOCATION ERROR'

    # Scraping location
    scraping_service_loc = scraping_service_scrape_location()
    scraping_service_loc = scraping_service_loc[
        'realitysk_location'] if 'error' not in scraping_service_loc else 'LOCATION ERROR'

    # Supported websites for scraping force update
    scraping_service_supported_websites_force_update = cache.get('scraping_service_supported_websites_force_update')
    scraping_service_supported_websites_force_update = scraping_service_supported_websites_force_update if scraping_service_supported_websites_force_update is not None else False

    context = {
        'segment': 'settings',
        'cities': get_cities(),
        'scraping_service_running': is_scraping_service_running(),
        'scraping_service_files_exist': do_scraping_service_files_exist(),
        'scraping_service_version': scraping_service_v,
        'scraping_service_scrape_interval': scraping_service_int,
        'scraping_service_location': scraping_service_loc,
        'scraping_service_supported_websites_force_update': scraping_service_supported_websites_force_update
    }

    html_template = loader.get_template('home/settings.html')
    return HttpResponse(html_template.render(context, request))


def stored_data(request):
    data = get_stored_data_from_database()

    # Get the value of per_page from the query string or default to 10
    per_page = int(request.GET.get('per_page', 10))

    paginator = Paginator(data, per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate start and end page numbers
    num_pages = paginator.num_pages
    current_page = page_obj.number
    start_page = max(1, current_page - 2)
    end_page = min(num_pages, current_page + 2)

    # Generate list of page numbers to display
    page_numbers = range(start_page, end_page + 1)

    context = {
        'segment': 'stored_data',
        'properties': page_obj,
        'page_numbers': page_numbers,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
    }

    html_template = loader.get_template('home/stored_data.html')
    return HttpResponse(html_template.render(context, request))


@csrf_exempt
@require_GET
def get_stored_data(request):
    try:
        print('test')
        data = get_stored_data_from_database(to_dict=True)
        return JsonResponse({'data': data}, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def scraping_service_status(request):
    # Scraping version
    scraping_service_v = scraping_service_version()
    scraping_service_v = scraping_service_v.lower() if 'error' not in scraping_service_v else 'VERSION ERROR'

    return JsonResponse({
        'scraping_service_version': scraping_service_v,
        'scraping_service_running': is_scraping_service_running(),
        'scraping_service_files_exists': do_scraping_service_files_exist()
    })


@csrf_exempt
def scraping_service_interval(request):
    try:
        if request.method == 'GET':
            fetched_interval = scraping_service_scrape_interval()
            if 'error' in fetched_interval:
                return JsonResponse({'error': fetched_interval['error']}, status=500)
            return JsonResponse(fetched_interval)
        elif request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            interval = data.get("scraping_interval_hours")
            fetched_interval = scraping_service_scrape_interval(interval)
            if isinstance(fetched_interval, dict) and 'error' in fetched_interval:
                return JsonResponse({'error': fetched_interval['error']}, status=500)
            return JsonResponse(fetched_interval)

    except Exception as e:
        print(f'Setting service interval error: {e}')
        return JsonResponse({'error': 'INTERVAL ERROR'}, status=500)


@csrf_exempt
def scraping_service_location(request):
    try:
        if request.method == 'GET':
            fetched_location = scraping_service_scrape_location()
            if 'error' in fetched_location:
                return JsonResponse({'error': fetched_location['error']}, status=500)
            return JsonResponse(fetched_location)
        elif request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            realitysk_location = data.get("realitysk_location")
            fetched_location = scraping_service_scrape_location(realitysk_location=realitysk_location)
            if 'error' in fetched_location:
                return JsonResponse({'error': fetched_location['error']}, status=500)
            return JsonResponse(fetched_location)
    except Exception as e:
        print(f'Setting service location error: {e}')
        return JsonResponse({'error': 'LOCATION ERROR'}, status=500)


@csrf_exempt
@require_POST
def scraping_service_website_support(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        force_update = data.get("force_update")
        fetched_supported_websites = scraping_service_supported_websites(force_update)
        if 'error' in fetched_supported_websites:
            return JsonResponse({'error': fetched_supported_websites['error']}, status=500)
        return JsonResponse(fetched_supported_websites)
    except Exception as e:
        print(f'Setting service location error: {e}')
        return JsonResponse({'error': 'SUPPORTED WEBSITES ERROR'}, status=500)


@csrf_exempt
@require_POST
def realitysk_scraping_service_scrape_today(request):
    try:
        fetched_record_scraping = realitysk_scraping_service_scrape_records(ScrapeDuration.TODAY)
        if 'error' in fetched_record_scraping:
            print(fetched_record_scraping['error'])
            return JsonResponse({'error': fetched_record_scraping['error']}, status=500)
        return JsonResponse(fetched_record_scraping)
    except Exception as e:
        print(f'Scraping realitysk data error: {e}')
        return JsonResponse({'error': 'SCRAPING REALITYSK DATA ERROR'}, status=500)


@csrf_exempt
@require_POST
def realitysk_scraping_service_scrape_all(request):
    try:
        fetched_record_scraping = realitysk_scraping_service_scrape_records(ScrapeDuration.ALL)
        if 'error' in fetched_record_scraping:
            return JsonResponse({'error': fetched_record_scraping['error']}, status=500)
        return JsonResponse(fetched_record_scraping)
    except Exception as e:
        print(f'Scraping realitysk data error: {e}')
        return JsonResponse({'error': 'SCRAPING REALITYSK DATA ERROR'}, status=500)


@csrf_exempt
@require_GET
def scraping_service_scrape_status(request):
    try:
        fetched_scrapers_status = scraping_service_scrapers_status()
        if 'error' in fetched_scrapers_status:
            return JsonResponse({'error': fetched_scrapers_status['error']}, status=500)
        return JsonResponse(fetched_scrapers_status)
    except Exception as e:
        print(f'Getting scrapers status error: {e}')
        return JsonResponse({'error': 'SCRAPE STATUS ERROR'}, status=500)


@csrf_exempt
@require_POST
def execute_scraping_service_action(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        action = data.get("action")

        if not action:
            raise ValueError("Action not provided in the request body")

        if system == "Windows":
            actions = {
                "install": installer_controller.install_windows,
                "start": installer_controller.start_windows,
                "restart": installer_controller.restart_windows,
                "stop": installer_controller.stop_windows,
                "uninstall": installer_controller.uninstall_windows,
                'train': model_trainer_controller.train_model
            }
        elif system == "Linux":
            actions = {
                "install": installer_controller.install_linux,
                "start": installer_controller.start_linux,
                "restart": installer_controller.restart_linux,
                "stop": installer_controller.stop_linux,
                "uninstall": installer_controller.uninstall_linux,
                'train': model_trainer_controller.train_model
            }
        else:
            raise NotImplementedError("Unsupported operating system")

        if action not in actions:
            raise NotImplementedError(f"Unsupported action: {action}")

        action_result = actions[action]()
        return JsonResponse({"message": action_result})
    except Exception as e:
        print(f'Setting service interval error: {e}')
        return JsonResponse({'error': 'An unexpected error occurred when performing service action.'}, status=500)


@csrf_exempt
@require_POST
def update_property(request):
    try:
        data = json.loads(request.body)
        print(data)

        property_id = data.get('id')
        field = data.get('field')
        new_value = data.get('newValue')

        if property_id is None or field is None or new_value is None:
            return JsonResponse({'error': 'Missing data for update: Ensure ID, field, and newValue are provided.'},
                                status=400)

        update_successful = update_database_property(property_id, field, new_value)

        if update_successful:
            return JsonResponse({'message': 'Property updated successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to update property. Check if the property ID exists.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        print(f'Error updating property: {e}')
        return JsonResponse({'error': 'An unexpected error occurred when updating property.'}, status=500)


def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
