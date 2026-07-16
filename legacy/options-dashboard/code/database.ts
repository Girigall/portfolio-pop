import { Database } from '@/integrations/supabase/types';

// Re-export core types from Supabase for convenience
export type DbTrade = Database['public']['Tables']['trades']['Row'];
export type DbInsertTrade = Database['public']['Tables']['trades']['Insert'];
export type DbOptionLeg = Database['public']['Tables']['option_legs']['Row'];
export type DbAttachment = Database['public']['Tables']['attachments']['Row'];
export type DbStrategyRule = Database['public']['Tables']['strategy_rules']['Row'];
export type DbAppSetting = Database['public']['Tables']['app_settings']['Row'];

// Filter types
export interface DashboardFilters {
  dateRange: { start: string | null; end: string | null };
  ticker: string | null;
  strategy: string | null;
  account: string | null;
  status: 'all' | 'open' | 'closed';
  exitType: string | null;
}

export interface DatasetFilters {
  dateRange: { start: string | null; end: string | null };
  ticker: string | null;
  status: 'all' | 'open' | 'closed';
  search: string;
}

// Rule engine types
export interface RuleValidationResult {
  pass: boolean;
  violations: string[];
  ruleScore: number;
  /** Verdict for UI display: 'adecuado' | 'revisar' | 'no_adecuado' */
  verdict?: VerdictStatus;
}

export type VerdictStatus = 'adecuado' | 'revisar' | 'no_adecuado';

// Trade candidate for validation
export interface TradeCandidate {
  ticker: string;
  strategy_name: string | null;
  number_of_contracts: number | null;
  credit_collected: number | null;
  short_strike: number | null;
  long_strike: number | null;
  spread_width: number | null;
  expiry_date: string | null;
  dte_at_entry: number | null;
  delta_short_leg: number | null;
  margin_requirement: number | null;
  underlying_price_at_entry: number | null;
  account_name: string | null;
  vix_on_entry: number | null;
  trend_condition: string | null;
  position_size_percent_of_portfolio: number | null;
}
