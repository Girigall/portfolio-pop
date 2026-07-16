import { StrategyRule } from '@/hooks/useTrades';
import { TradeCandidate, RuleValidationResult, VerdictStatus } from '@/types/database';

/**
 * Deterministic Rule Engine for validating options trades
 * against configured strategy rules.
 *
 * Returns pass/fail, detailed violations, and a UI-friendly verdict.
 */

export function validateTradeAgainstRules(
  trade: TradeCandidate,
  rules: StrategyRule
): RuleValidationResult {
  const violations: string[] = [];
  let passedChecks = 0;
  let totalChecks = 0;

  // Check 1: DTE between min and max
  if (rules.min_dte != null && rules.max_dte != null && trade.dte_at_entry != null) {
    totalChecks++;
    if (trade.dte_at_entry < rules.min_dte) {
      violations.push(`DTE (${trade.dte_at_entry}) below minimum (${rules.min_dte})`);
    } else if (trade.dte_at_entry > rules.max_dte) {
      violations.push(`DTE (${trade.dte_at_entry}) exceeds maximum (${rules.max_dte})`);
    } else {
      passedChecks++;
    }
  }

  // Check 2: Delta short leg between min and max
  if (rules.min_delta_short != null && rules.max_delta_short != null && trade.delta_short_leg != null) {
    totalChecks++;
    const absDelta = Math.abs(trade.delta_short_leg);
    if (absDelta < rules.min_delta_short) {
      violations.push(`Delta (${absDelta.toFixed(2)}) below minimum (${rules.min_delta_short})`);
    } else if (absDelta > rules.max_delta_short) {
      violations.push(`Delta (${absDelta.toFixed(2)}) exceeds maximum (${rules.max_delta_short})`);
    } else {
      passedChecks++;
    }
  }

  // Check 3: Spread width matches required
  if (rules.required_spread_width != null && trade.spread_width != null) {
    totalChecks++;
    if (trade.spread_width !== rules.required_spread_width) {
      violations.push(`Spread width ($${trade.spread_width}) does not match required ($${rules.required_spread_width})`);
    } else {
      passedChecks++;
    }
  }

  // Check 4: Credit collected within range
  if (rules.min_credit != null && rules.max_credit != null && trade.credit_collected != null) {
    totalChecks++;
    if (trade.credit_collected < rules.min_credit) {
      violations.push(`Credit ($${trade.credit_collected}) below minimum ($${rules.min_credit})`);
    } else if (trade.credit_collected > rules.max_credit) {
      violations.push(`Credit ($${trade.credit_collected}) exceeds maximum ($${rules.max_credit})`);
    } else {
      passedChecks++;
    }
  }

  // Check 5: Credit-to-width ratio
  if (rules.min_credit_to_width_ratio != null && rules.max_credit_to_width_ratio != null && 
      trade.credit_collected != null && trade.spread_width != null && trade.spread_width > 0) {
    totalChecks++;
    const ratio = trade.credit_collected / trade.spread_width;
    if (ratio < rules.min_credit_to_width_ratio) {
      violations.push(`Credit/width ratio (${ratio.toFixed(3)}) below minimum (${rules.min_credit_to_width_ratio})`);
    } else if (ratio > rules.max_credit_to_width_ratio) {
      violations.push(`Credit/width ratio (${ratio.toFixed(3)}) exceeds maximum (${rules.max_credit_to_width_ratio})`);
    } else {
      passedChecks++;
    }
  }

  // Check 6: Position size within limit
  if (rules.max_position_size_percent != null && trade.position_size_percent_of_portfolio != null) {
    totalChecks++;
    if (trade.position_size_percent_of_portfolio > rules.max_position_size_percent) {
      violations.push(`Position size (${trade.position_size_percent_of_portfolio}%) exceeds maximum (${rules.max_position_size_percent}%)`);
    } else {
      passedChecks++;
    }
  }

  // Check 7: VIX within limit
  if (rules.max_vix_for_entry != null && trade.vix_on_entry != null) {
    totalChecks++;
    if (trade.vix_on_entry > rules.max_vix_for_entry) {
      violations.push(`VIX (${trade.vix_on_entry}) exceeds maximum (${rules.max_vix_for_entry})`);
    } else {
      passedChecks++;
    }
  }

  // Check 8: Trend condition for put credit spreads
  if (
    rules.allowed_trend_for_put_spreads &&
    rules.allowed_trend_for_put_spreads.length > 0 &&
    trade.strategy_name?.toLowerCase().includes('put') &&
    trade.trend_condition
  ) {
    totalChecks++;
    if (!rules.allowed_trend_for_put_spreads.includes(trade.trend_condition)) {
      violations.push(`Trend condition (${trade.trend_condition}) not allowed for put spreads (allowed: ${rules.allowed_trend_for_put_spreads.join(', ')})`);
    } else {
      passedChecks++;
    }
  }

  // Check 9: Target index filter
  if (rules.target_index && trade.ticker) {
    totalChecks++;
    if (trade.ticker !== rules.target_index && !trade.ticker?.startsWith(rules.target_index)) {
      violations.push(`Ticker (${trade.ticker}) does not match target index (${rules.target_index})`);
    } else {
      passedChecks++;
    }
  }

  // Calculate rule score (0-100)
  const ruleScore = totalChecks > 0 ? Math.round((passedChecks / totalChecks) * 100) : 100;

  // Determine verdict for UI display
  const hasViolations = violations.length > 0;
  let verdict: VerdictStatus;
  if (!hasViolations) {
    verdict = 'adecuado';
  } else if (ruleScore >= 50) {
    verdict = 'revisar';
  } else {
    verdict = 'no_adecuado';
  }

  return {
    pass: violations.length === 0,
    violations,
    ruleScore,
    verdict,
  };
}

/**
 * Get validation status label based on rule result
 * Returns 'pass' | 'warning' | 'fail' for backward compatibility
 */
export function getValidationStatus(result: RuleValidationResult): 'pass' | 'warning' | 'fail' {
  if (result.pass) return 'pass';
  if (result.ruleScore >= 50) return 'warning';
  return 'fail';
}

/**
 * Get the UI-friendly verdict emoji/label for a validation result.
 */
export function getVerdictDisplay(verdict?: VerdictStatus): { icon: string; label: string; color: string } {
  switch (verdict) {
    case 'adecuado':
      return { icon: '✅', label: 'Adecuado', color: 'text-profit' };
    case 'revisar':
      return { icon: '🔶', label: 'Revisar', color: 'text-warning' };
    case 'no_adecuado':
      return { icon: '🔴', label: 'No adecuado', color: 'text-loss' };
    default:
      return { icon: '—', label: 'Sin evaluar', color: 'text-muted-foreground' };
  }
}

/**
 * Calculate rule compliance percentage for a set of trades
 */
export function calculateRuleCompliancePercent(
  trades: Array<{ entry_rule_pass: boolean | null }>
): number {
  const validatedTrades = trades.filter(t => t.entry_rule_pass !== null);
  if (validatedTrades.length === 0) return 100;
  
  const passingTrades = validatedTrades.filter(t => t.entry_rule_pass === true).length;
  return (passingTrades / validatedTrades.length) * 100;
}
