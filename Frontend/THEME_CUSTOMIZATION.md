# Rakshika-Ai Theme Customization Guide

## Rakshika-Ai
The Rakshika-Ai application now uses a **centralized, professional theme** based on women's safety empowerment. All pages automatically inherit consistent styling through the `theme.py` module.

## 📁 Theme File
- **Location:** `Frontend/theme.py`
- **Functions:** 
  - `apply_global_theme()` - Applies theme to all pages
  - `auth_page_setup()` - Special styling for login/register pages
  - `metric_card()` - Styled metric display component
  - `info_box()` - Styled information box component

## 🎨 Color Palette

### Primary Colors (Safety & Trust)
```python
"primary": "#6B46C1"          # Deep Purple
"primary_light": "#8B5CF6"    # Light Purple
"primary_dark": "#5A36A3"     # Dark Purple
```

### Secondary Colors (Emergency & Action)
```python
"danger": "#DC2626"           # Bright Red
"danger_light": "#EF4444"     # Light Red
"danger_dark": "#B91C1C"      # Dark Red
```

### Accent Colors (Hope & Empowerment)
```python
"accent": "#DB2777"           # Deep Rose
"accent_light": "#EC4899"     # Light Rose
```

### Support Colors
```python
"success": "#10B981"          # Teal/Green
"success_light": "#34D399"    # Light Teal
```

### Neutral Colors
```python
"bg_light": "#F9FAFB"         # Almost white
"bg_medium": "#F3F4F6"        # Light gray
"bg_dark": "#1F2937"          # Dark gray
"text_dark": "#111827"        # Almost black
"text_light": "#6B7280"       # Gray
"text_white": "#FFFFFF"       # White
```

## 🚀 How to Use

### 1. **In Any Streamlit Page**
```python
import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from theme import apply_global_theme

st.set_page_config(...)

# Apply the theme globally
apply_global_theme()
```

### 2. **For Authentication Pages (Login/Register)**
```python
from theme import apply_global_theme, auth_page_setup

st.set_page_config(...)

# This applies authentication-specific styling
auth_page_setup("Login")
apply_global_theme()
```

### 3. **Using Metric Cards**
```python
from theme import metric_card

# Display a metric with icon
metric_card("Total Cases", "1,234", "📊")
metric_card("Safety Score", "85%", "🛡️")
```

### 4. **Using Info Boxes**
```python
from theme import info_box

# Display an info box
info_box("Important", "This is important information", "⚠️")
```

## 🎯 What Gets Styled Automatically

✅ **Global styling includes:**
- Background gradients
- Headers (h1-h6) with gradient text effect
- Buttons with hover effects
- Text inputs with focus states
- Sidebar with purple gradient
- Tables with header gradient
- Tabs with active state indicators
- Sliders with custom track
- Chat messages (user vs assistant)
- Success/Error/Warning boxes
- Custom scrollbars
- Cards and containers
- Responsive design for mobile

## 🔄 Customizing the Theme

### Option 1: Modify Color Palette
Edit `theme.py` line 6-30 to change colors globally:

```python
COLORS = {
    "primary": "#YOUR_COLOR",
    "accent": "#YOUR_COLOR",
    # ... etc
}
```

### Option 2: Override Specific Styles
Add custom CSS after calling `apply_global_theme()`:

```python
st.markdown("""
<style>
.custom-class {
    color: red;
}
</style>
""", unsafe_allow_html=True)
```

### Option 3: Create Page-Specific Themes
Create separate functions in `theme.py` for specific page themes:

```python
def apply_dashboard_theme():
    """Dashboard-specific theme"""
    st.markdown("""<style>...""", unsafe_allow_html=True)
```

## 📱 Responsive Design
The theme automatically handles:
- Mobile devices (< 640px)
- Tablets (640px - 1024px)
- Desktop (> 1024px)

Adjustments are made for:
- Font sizes
- Padding/margins
- Container widths
- Column layouts

## 🎨 Theme Components

### Metric Cards
- Gradient background (Primary → Light Primary)
- White text
- Centered content
- Hover lift effect
- Shadow effect

### Buttons
- Gradient background
- White text
- Rounded corners (8px)
- Hover transform (lift effect)
- Enhanced shadow on hover

### Input Fields
- Light gray background
- 2px border (primary on focus)
- Rounded corners (8px)
- Smooth transitions
- Focus ring effect

### Sidebar
- Gradient background (Dark Purple → Primary)
- White text
- Better contrast

## 🔗 Updated Pages

All pages now use the theme:
1. ✅ `pages/1_login.py` - Auth page styling
2. ✅ `pages/2_dashboard.py` - Global theme
3. ✅ `pages/3_Dataset.py` - Global theme
4. ✅ `pages/5_Safety_Map.py` - Global theme
5. ✅ `pages/6_GlobalChat.py` - Global theme
6. ✅ `pages/7_About.py` - Global theme
7. ✅ `pages/8_Register.py` - Auth page styling
8. ✅ `app.py` - Global theme

## 💡 Pro Tips

1. **Consistency**: Always call `apply_global_theme()` at the top of new pages
2. **Performance**: Theme is applied once per page load, so it's lightweight
3. **Accessibility**: The theme uses sufficient color contrast (WCAG AA compliant)
4. **Brand Colors**: The purple/rose palette conveys trust, safety, and empowerment
5. **Testing**: Test on mobile devices to ensure responsive design works

## 🐛 Troubleshooting

**Issue**: Styles not applying
- **Solution**: Make sure `apply_global_theme()` is called before other content

**Issue**: Conflicting styles
- **Solution**: Increase CSS specificity or use `!important` (sparingly)

**Issue**: Colors look different on different devices
- **Solution**: This is normal due to screen calibration. Theme uses web-safe colors

## 📝 Example: Complete Page Setup

```python
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from theme import apply_global_theme, metric_card, info_box

st.set_page_config(page_title="My Page", layout="wide")
apply_global_theme()

# Your content
st.title("Welcome to Rakshika-Ai")
st.markdown("Your safe space for information and support")

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Active Users", "2,500", "👥")
with col2:
    metric_card("Resources", "150+", "📚")
with col3:
    metric_card("Safety Score", "92%", "🛡️")

info_box("Getting Started", 
         "Explore our safety resources and connect with the community",
         "ℹ️")
```

## 🌟 Next Steps

1. Test the theme on all pages
2. Provide feedback on colors or styling
3. Customize the palette to match your brand guidelines
4. Add page-specific themes if needed
5. Extend theme with new component functions

---

**Theme Created:** April 2026  
**For:** Rakshika-Ai - Women's Safety Analytics Platform
