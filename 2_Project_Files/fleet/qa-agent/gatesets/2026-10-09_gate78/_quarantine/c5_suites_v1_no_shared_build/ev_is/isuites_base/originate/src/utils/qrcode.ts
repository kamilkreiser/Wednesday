/**
 * =============================================================================
 * QR CODE UTILITIES
 * =============================================================================
 * QR code generation for document verification
 * =============================================================================
 */

import QRCode from 'qrcode';

/**
 * Generate QR code as base64-encoded PNG
 * @param data - Data to encode in QR code
 * @returns Base64-encoded PNG string
 */
export async function generateQRCode(data: string): Promise<string> {
  const options: QRCode.QRCodeToDataURLOptions = {
    errorCorrectionLevel: 'M',
    type: 'image/png',
    margin: 2,
    width: 256,
    color: {
      dark: '#000000',
      light: '#FFFFFF',
    },
  };

  return QRCode.toDataURL(data, options);
}

/**
 * Generate QR code as SVG string
 * @param data - Data to encode in QR code
 * @returns SVG string
 */
export async function generateQRCodeSVG(data: string): Promise<string> {
  const options: QRCode.QRCodeToStringOptions = {
    errorCorrectionLevel: 'M',
    type: 'svg',
    margin: 2,
    width: 256,
  };

  return QRCode.toString(data, options);
}

/**
 * Generate QR code as Buffer
 * @param data - Data to encode in QR code
 * @returns PNG buffer
 */
export async function generateQRCodeBuffer(data: string): Promise<Buffer> {
  const options: QRCode.QRCodeToBufferOptions = {
    errorCorrectionLevel: 'M',
    type: 'png',
    margin: 2,
    width: 256,
  };

  return QRCode.toBuffer(data, options);
}
