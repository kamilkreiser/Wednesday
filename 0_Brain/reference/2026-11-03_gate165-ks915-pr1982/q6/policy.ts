const MIN_LENGTH_DEFAULT = 12;
const MIN_LENGTH_ADMIN = 14;
export interface PasswordStrength {
  score: number;  // 0-4
  feedback: string[];
  isStrong: boolean;
}

export function checkPasswordStrength(
  password: string,
  options: { minLength?: number } = {},
): PasswordStrength {
  // Pen-test F-12 fix: floor raised from 8 → 12 (default), 14 for admins.
  const minLength = options.minLength ?? MIN_LENGTH_DEFAULT;
  const feedback: string[] = [];
  let score = 0;

  // Length check
  if (password.length >= minLength) score++;
  if (password.length >= minLength + 2) score++;
  if (password.length < minLength) feedback.push(`Password must be at least ${minLength} characters`);
  
  // Character variety — require at least 3 of 4 categories
  const hasLower = /[a-z]/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasDigit = /[0-9]/.test(password);
  const hasSpecial = /[^a-zA-Z0-9]/.test(password);
  
  if (hasLower) score += 0.5;
  else feedback.push('Add lowercase letters');
  
  if (hasUpper) score += 0.5;
  else feedback.push('Add uppercase letters');
  
  if (hasDigit) score += 0.5;
  else feedback.push('Add numbers');
  
  if (hasSpecial) score += 0.5;
  else feedback.push('Add special characters');
  
  const categoriesMet = [hasLower, hasUpper, hasDigit, hasSpecial].filter(Boolean).length;
  if (categoriesMet < 3) {
    feedback.push('Use at least 3 of: lowercase, uppercase, numbers, special characters');
  }
  
  // Common patterns to avoid
  const commonPatterns = [
    /^123456/,
    /password/i,
    /qwerty/i,
    /letmein/i,
    /welcome/i,
    /admin/i,
    /^(.)\1+$/,  // Repeated characters
    /^(012|123|234|345|456|567|678|789)/,  // Sequential digits
    /^(abc|bcd|cde|def)/i,  // Sequential letters
  ];
  
  for (const pattern of commonPatterns) {
    if (pattern.test(password)) {
      score = Math.max(0, score - 1);
      feedback.push('Avoid common patterns and dictionary words');
      break;
    }
  }
  
  // Require minimum length AND at least 3 character categories to be "strong"
  const isStrong = password.length >= minLength && categoriesMet >= 3 && score >= 3;

  return {
    score: Math.min(4, Math.floor(score)),
    feedback,
    isStrong,
  };
}

/**
 * Helper: minimum length for a given role. SYSTEM_ADMIN / PLATFORM_ADMIN
 * get 14, everyone else gets 12. Use in registration / password-reset
 * validators.
 */
export function minLengthForRole(role: string | undefined): number {
  if (!role) return MIN_LENGTH_DEFAULT;
  const upper = role.toUpperCase();
  if (upper === 'SYSTEM_ADMIN' || upper === 'PLATFORM_ADMIN') return MIN_LENGTH_ADMIN;
  return MIN_LENGTH_DEFAULT;
}
