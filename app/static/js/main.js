// PaletteVault - barcode scanner modal (home page)

function openScanner() {
  document.getElementById('scannerModal').style.display = 'flex';
}

function closeScanner() {
  document.getElementById('scannerModal').style.display = 'none';
}

function simulateScan() {
  document.getElementById('barcodeInput').value = '5060123456789 - NARS Concealer Auto-Detected';
  closeScanner();
}
