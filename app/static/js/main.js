// PaletteVault - barcode scanner modal (home page)

function openScanner() {
  document.getElementById('scannerModal').style.display = 'flex';
}

function closeScanner() {
  document.getElementById('scannerModal').style.display = 'none';
}

// The camera is still simulated: fill in a barcode that exists in the
// database (NARS Radiant Creamy Concealer) and submit it for lookup.
function simulateScan() {
  document.getElementById('barcodeInput').value = '2100000079193';
  closeScanner();
  document.getElementById('scanForm').submit();
}
