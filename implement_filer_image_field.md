# Implementation Task: Replace Tab Image Dropdown with FilerImageField

## Objective
Replace the current simple dropdown image selection in the Bootstrap4 Tabs plugin with a proper Filer-driven image selection field that provides the same user experience as DjangoCMS-Picture.

## Current Implementation Analysis

### Current File Location
- **File:** `/Users/wbomar/Code/TACC/Texascale-CMS/cms/src/texascale_custom/djangocms_bootstrap4_tabs/extend.py`
- **Lines:** 1-206

### Current Problems
1. **Poor UX:** Simple dropdown with all images in system (not scalable)
2. **No Visual Preview:** Users can't see image thumbnails
3. **No Filer Integration:** Missing folder navigation, search, upload capabilities
4. **Complex Data Handling:** Images stored as JSON in `attributes['data-tab-image-id']`

### Current Data Flow
- Form field: `forms.ModelChoiceField` with `forms.Select` widget
- Storage: Image ID stored in `attributes['data-tab-image-id']` JSON field
- Retrieval: Complex property methods to convert ID back to Image object

## Target Implementation

### Reference Pattern
Based on analysis of `djangocms-picture` v3.0.0:
- **Model:** Uses `FilerImageField` directly on model
- **Form:** No custom widget needed - `FilerImageField` provides automatic widget
- **Storage:** Direct ForeignKey relationship to `filer.models.Image`

### Key Implementation Files
```python
# Reference: https://raw.githubusercontent.com/django-cms/djangocms-picture/refs/tags/3.0.0/djangocms_picture/models.py
picture = FilerImageField(
    verbose_name=_('Image'),
    blank=True,
    null=True,
    on_delete=models.SET_NULL,
    related_name='+',
)

# Reference: https://raw.githubusercontent.com/django-cms/djangocms-picture/refs/tags/3.0.0/djangocms_picture/forms.py
class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'
        # No custom widget - FilerImageField handles this automatically!
```

## Implementation Tasks

### Task 1: Update Model Definition

**Current Code (lines ~108-150):**
```python
class Bootstrap4TabItemModel(OriginalBootstrap4TabItem):
    class Meta:
        proxy = True
    # ... complex attribute handling ...
```

**Required Changes:**
1. **Add FilerImageField import:**
   ```python
   from filer.fields.image import FilerImageField
   ```

2. **Change model to non-proxy and add field:**
   ```python
   class Bootstrap4TabItemModel(OriginalBootstrap4TabItem):
       tab_image = FilerImageField(
           verbose_name=_('Tab Image/Thumbnail'),
           blank=True,
           null=True,
           on_delete=models.SET_NULL,
           related_name='+',
           help_text=_('Optional image to display in the tab title for slideshow navigation')
       )
       
       class Meta:
           proxy = False  # CRITICAL: Change from True to False
   ```

3. **Remove complex property methods** - no longer needed with direct field access

### Task 2: Simplify Form Implementation

**Current Code (lines ~60-107):**
```python
class Bootstrap4TabItemForm(forms.ModelForm):
    tab_image = forms.ModelChoiceField(
        queryset=Image.objects.all(),
        required=False,
        # ... complex widget configuration ...
    )
    # ... complex __init__ and save methods ...
```

**Required Changes:**
1. **Simplify form to use automatic widget:**
   ```python
   class Bootstrap4TabItemForm(forms.ModelForm):
       class Meta:
           model = Bootstrap4TabItemModel
           fields = '__all__'
           # FilerImageField automatically provides the correct widget!
       
       # Remove complex __init__ and save methods - no longer needed
   ```

### Task 3: Update Plugin Render Method

**Current Code (lines ~180-206):**
```python
def render(self, context, instance, placeholder):
    # ... complex attribute parsing ...
    try:
        tab_image = Image.objects.get(id=instance.attributes['data-tab-image-id'])
    except (Image.DoesNotExist, ValueError, TypeError):
        # ... error handling ...
```

**Required Changes:**
1. **Simplify render method:**
   ```python
   def render(self, context, instance, placeholder):
       context = super().render(context, instance, placeholder)
       
       context.update({
           'tab_image': instance.tab_image,  # Direct field access!
           'has_tab_image': bool(instance.tab_image),
           'filtered_attributes_str': filter_attributes_str(instance.attributes or {})
       })
       
       return context
   ```

### Task 4: Update Template (tabs_image.html)

**Current Template:**
```django
<img
    src="{{ image.url }}"
    srcset="{{ image.url }} {{ image.width }}w"
    alt="{{ image.default_alt_text|default:plugin.tab_title }}"

    {% if image.subject_location %}
    data-subject-location="{{ image.subject_location }}"
    {% endif %}

    {% if image.default_caption %}
    title="{{ image.default_caption }}"
    {% endif %}

    loading="lazy"
>
```

**Updated Template (following djangocms-picture pattern):**
```django
<img src="{{ image.url }}"
    alt="{% if image.default_alt_text %}{{ image.default_alt_text }}{% else %}{{ plugin.tab_title }}{% endif %}"
    {% if image.width %} width="{{ image.width }}"{% endif %}
    {% if image.height %} height="{{ image.height }}"{% endif %}
    {% if image.subject_location %} data-subject-location="{{ image.subject_location }}"{% endif %}
    {% if image.default_caption %} title="{{ image.default_caption }}"{% endif %}
    loading="lazy"
>
```

### Task 5: Remove Obsolete Code

**Remove these functions/methods (no longer needed):**
1. `validate_tab_image()` function (lines ~18-38)
2. `filter_attributes_str()` function (lines ~40-58) - if only used for tab images
3. Complex `__init__` method in form (lines ~75-87)
4. Complex `clean()` method in form (lines ~89-94)
5. Complex `save()` method in form (lines ~96-107)
6. Complex `tab_image` property in model (lines ~125-135)
7. Complex `tab_image.setter` in model (lines ~137-147)
8. Complex `clean()` method in model (lines ~149-152)

### Task 6: Create Migration

**Generate migration:**
```bash
python manage.py makemigrations texascale_custom
```

**Note:** Since this is sandbox environment, no data migration needed. Existing tab images will be lost, which is acceptable per requirements.

## Validation Requirements

### Functional Testing
- [ ] **Image Selection:** Widget opens Filer's visual browser interface
- [ ] **Image Preview:** Selected images display thumbnail previews in form
- [ ] **Data Persistence:** Images are correctly saved to new `tab_image` field
- [ ] **Template Rendering:** Images display correctly in frontend templates with updated template
- [ ] **Migration Success:** Migration runs without errors

### Template Compatibility
The main template (`tabs.html`) should continue to work since it already accesses `plugin.tab_image`:

```django
{# In tabs.html - this should continue working #}
{% if plugin.tab_image %}
    {% include "./tabs_image.html" with image=plugin.tab_image %}
{% else %}
    {{ plugin.tab_title }}
{% endif %}
```

The `tabs_image.html` template will be updated to follow djangocms-picture patterns.

### Error Handling
- [ ] **Missing Images:** Handle cases where Filer images are deleted (automatic with FilerImageField)
- [ ] **Form Validation:** Verify field validation works as expected
- [ ] **Clean Migration:** Ensure migration creates new field structure correctly

## Success Criteria

1. **User Experience:** Image selection provides same UX as DjangoCMS-Picture
2. **Code Simplicity:** Significantly reduced code complexity (remove ~100+ lines of complex logic)
3. **Performance:** No performance regression in admin or frontend
4. **Template Quality:** Updated template follows djangocms-picture best practices
5. **Migration Success:** Clean migration to new field structure

## Notes

- **Critical:** Change `proxy = True` to `proxy = False` in model Meta class
- **Migration:** This will require a database migration
- **Data Loss:** Existing tab images will be lost (acceptable for sandbox environment)
- **Template Update:** `tabs_image.html` needs to be updated to follow djangocms-picture pattern
- **Dependencies:** Verify `filer` package is properly installed and configured

## Expected Outcome

After implementation, users will have the same rich image selection experience as DjangoCMS-Picture, with visual thumbnails, folder navigation, search capabilities, and direct upload functionality. The codebase will be significantly simplified with proper Django patterns, and the template will follow established djangocms-picture conventions.