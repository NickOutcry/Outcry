# Adding Futura Light Font to jsPDF

## Method 1: Using a TTF Font File (Recommended)

1. **Obtain the Futura Light font file**:
   - You need a legal copy of Futura Light in TTF format
   - Place it in this directory as `Futura-Light.ttf`

2. **The font will be automatically loaded**:
   - The `font-loader.js` script will automatically load the font
   - It will be available as 'futura-light' in jsPDF

## Method 2: Using a Web Font

If you have access to Futura Light as a web font, you can modify the `font-loader.js` file to load it from a CDN or your own server.

## Method 3: Using a Similar Font

If you don't have access to Futura Light, you can use a similar font:

### Free Alternatives:
- **Montserrat Light** (Google Fonts)
- **Open Sans Light** (Google Fonts)
- **Lato Light** (Google Fonts)

### To use a Google Font:
1. Add the font to your HTML:
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap" rel="stylesheet">
```

2. Modify the font loader to use the alternative font.

## Current Implementation

The current code will:
1. Try to load Futura Light from `/static/fonts/Futura-Light.ttf`
2. Fall back to Helvetica if the font is not available
3. Log messages to the console about font loading status

## Testing

To test if the font is loaded:
1. Open the browser developer console
2. Generate a PDF
3. Look for console messages about font loading
4. Check if the staff information uses the correct font

## Legal Note

Make sure you have the proper license to use Futura Light in your application. If you don't have a license, use one of the free alternatives mentioned above.






