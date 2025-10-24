// Font Loader for jsPDF
// This file handles loading custom fonts into jsPDF

// Function to load Futura Light font into jsPDF
async function loadFuturaLightFont() {
    try {
        // Check if jsPDF is available
        if (typeof window.jspdf === 'undefined') {
            console.warn('jsPDF not available for font loading');
            return false;
        }

        const { jsPDF } = window.jspdf;
        
        // Check if font is already loaded
        const testDoc = new jsPDF();
        const fontList = testDoc.getFontList();
        
        if (fontList && fontList['Futura Light BT']) {
            console.log('Futura Light BT font already loaded');
            return true;
        }

        // Try to load the font file
        try {
            // Load the font file (you need to add Futura-Light.ttf to static/fonts/)
            const fontResponse = await fetch('/static/fonts/Futura-Light.ttf');
            if (fontResponse.ok) {
                const fontArrayBuffer = await fontResponse.arrayBuffer();
                const fontBase64 = arrayBufferToBase64(fontArrayBuffer);
                
                // Add the font to jsPDF
                jsPDF.API.events.push(['addFonts', function() {
                    this.addFileToVFS('Futura-Light.ttf', fontBase64);
                    this.addFont('Futura-Light.ttf', 'Futura Light BT', 'normal');
                }]);
                
                console.log('Futura Light BT font loaded successfully');
                return true;
            } else {
                console.warn('Futura Light BT font file not found');
                return false;
            }
        } catch (error) {
            console.warn('Error loading Futura Light BT font:', error);
            return false;
        }
    } catch (error) {
        console.error('Error in loadFuturaLightFont:', error);
        return false;
    }
}

// Helper function to convert ArrayBuffer to Base64
function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

// Alternative: Load font from a CDN or external source
async function loadFuturaLightFromCDN() {
    try {
        if (typeof window.jspdf === 'undefined') {
            return false;
        }

        const { jsPDF } = window.jspdf;
        
        // Example: Load from Google Fonts or other CDN
        // This is just an example - you'd need to find a reliable source
        const fontUrl = 'https://fonts.gstatic.com/s/futura/v1/...'; // Replace with actual URL
        
        const fontResponse = await fetch(fontUrl);
        if (fontResponse.ok) {
            const fontArrayBuffer = await fontResponse.arrayBuffer();
            const fontBase64 = arrayBufferToBase64(fontArrayBuffer);
            
            jsPDF.API.events.push(['addFonts', function() {
                this.addFileToVFS('Futura-Light.ttf', fontBase64);
                this.addFont('Futura-Light.ttf', 'Futura Light BT', 'normal');
            }]);
            
            console.log('Futura Light BT font loaded from CDN');
            return true;
        }
    } catch (error) {
        console.warn('Error loading Futura Light BT from CDN:', error);
        return false;
    }
    return false;
}

// Initialize font loading when the page loads
document.addEventListener('DOMContentLoaded', async function() {
    // Try to load Futura Light BT font
    await loadFuturaLightFont();
});

// Export functions for use in other scripts
window.FontLoader = {
    loadFuturaLightFont,
    loadFuturaLightFromCDN
};
