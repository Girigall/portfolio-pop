export interface Trade {
  id: string;
  ticker: string;
  numberOfContracts: number;
  entryPrice: number;
  shortStrike: number;
  longStrike: number;
  spreadWidth: number;
  expiryDate: string;
  entryDate: string;
  dteAtEntry: number;
  creditCollected: number;
  creditToWidthRatio: number;
  deltaShortLeg: number;
  vixOnEntry: number;
  expectedMoveForCycle: number;
  breakevenPoints: number;
  breakevenCushionPoints: number;
  breakevenCushionPercent: number;
  twentyMAStatus: 'above' | 'below' | 'at';
  fiftyMAStatus: 'above' | 'below' | 'at';
  trendCondition: 'bullish' | 'bearish' | 'neutral';
  reasonForEntry: string;
  timeOfEntry: string;
  marketStructure: string;
  entryQualityScore: number;
  positionSizeAsPercentOfPortfolio: number;
  marginRequirement: number;
  exitDate: string | null;
  exitPremium: number | null;
  exitType: 'profit_target' | 'stop_loss' | 'expiry' | 'manual' | null;
  daysInTrade: number | null;
  reasonForExit: string | null;
  plDollar: number | null;
  plrMultiple: number | null;
  didPriceTouchShortStrike: boolean | null;
  trendConditionAtExit: 'bullish' | 'bearish' | 'neutral' | null;
  vixChangeDuringTrade: number | null;
  notes: string | null;
}

export interface Attachment {
  id: string;
  tradeId: string;
  imageUrl: string;
  createdAt: string;
  description: string | null;
}

export interface DashboardFilters {
  dateRange: { start: string | null; end: string | null };
  ticker: string | null;
  exitType: string | null;
}

export interface DatasetFilters {
  dateRange: { start: string | null; end: string | null };
  ticker: string | null;
  status: 'all' | 'open' | 'closed';
  search: string;
}

export type SortDirection = 'asc' | 'desc';

export interface SortConfig {
  key: keyof Trade;
  direction: SortDirection;
}
