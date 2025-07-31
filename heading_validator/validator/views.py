from django.shortcuts import render
from bs4 import BeautifulSoup
from django.views.decorators.http import require_http_methods

# Create your views here.



@require_http_methods(["GET", "POST"])
def validate_headings(request):
    if request.method == "POST":
        html_content = request.POST.get('html_content', '')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract all headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        # Analyze hierarchy
        errors = []
        previous_level = 0
        
        for i, heading in enumerate(headings):
            current_level = int(heading.name[1])
            
            # Check for skipping levels (e.g., h1 to h3)
            if i > 0 and current_level > previous_level + 1:
                errors.append(
                    f"Heading hierarchy jump from h{previous_level} to h{current_level} "
                    f"at position {i+1}: '{heading.text.strip()}'"
                )
            
            previous_level = current_level
        
        # Check for multiple h1s
        h1s = soup.find_all('h1')
        if len(h1s) > 1:
            errors.append(f"Multiple h1 tags found ({len(h1s)}). Typically only one h1 should exist.")
        
        context = {
            'html_content': html_content,
            'headings': [{'level': int(h.name[1]), 'text': h.text.strip()} for h in headings],
            'errors': errors,
            'is_valid': len(errors) == 0
        }
        return render(request, 'results.html', context)
    
    return render(request, 'index.html')