// Friendly names for the types generated from the FastAPI OpenAPI spec (npm run api:types)
import type { components } from "./schema";

type Schemas = components["schemas"];

export type Sample = Schemas["SampleOut"];
export type DocumentInfo = Schemas["DocumentOut"];

export type InvoiceSummary = Schemas["InvoiceSummary"];
export type InvoiceDetail = Schemas["InvoiceDetail"];
export type InvoiceUpdate = Schemas["InvoiceUpdate"];
export type InvoiceStatus = InvoiceSummary["status"];
export type Line = Schemas["LineOut"];
export type LineInput = Schemas["LineIn"];
export type Flag = Schemas["FlagOut"];

export type InventoryItem = Schemas["InventoryItemOut"];
export type Movement = Schemas["MovementOut"];
export type Spending = Schemas["SpendingOut"];
export type Stats = Schemas["StatsOut"];

export type ExportFormat = "csv" | "json";