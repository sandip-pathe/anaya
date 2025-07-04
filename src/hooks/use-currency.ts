import { useEffect, useState } from "react";

interface CurrencyInfo {
  symbol: string;
  price: number;
  currency: string;
  display: string;
}

export const useRegionalCurrency = (): CurrencyInfo => {
  const [currencyInfo, setCurrencyInfo] = useState<CurrencyInfo>({
    symbol: "$",
    price: 10,
    currency: "USD",
    display: "$10 USD",
  });

  useEffect(() => {
    const detectCurrency = () => {
      const locale = navigator.language || "en-US";
      const region = locale.split("-")[1]?.toUpperCase() || "US";

      let price = 10;
      let currency = "USD";
      let symbol = "$";

      switch (region) {
        case "US":
        case "CA":
        case "AU":
        case "NZ":
          price = 10;
          currency = "USD";
          symbol = "$";
          break;

        case "IN":
        case "PK":
        case "BD":
        case "LK":
          price = 500;
          currency = "INR";
          symbol = "₹";
          break;

        case "SG":
        case "MY":
        case "ID":
        case "PH":
        case "TH":
        case "VN":
          price = 15;
          currency = "SGD";
          symbol = "S$";
          break;

        case "GB":
          price = 8;
          currency = "GBP";
          symbol = "£";
          break;

        case "DE":
        case "FR":
        case "IT":
        case "ES":
        case "NL":
        case "SE":
        case "FI":
        case "NO":
          price = 9;
          currency = "EUR";
          symbol = "€";
          break;

        case "ZA":
        case "NG":
        case "KE":
          price = 10;
          currency = "USD";
          symbol = "$";
          break;

        default:
          price = 10;
          currency = "USD";
          symbol = "$";
      }

      setCurrencyInfo({
        symbol,
        price,
        currency,
        display: `${symbol}${price} ${currency}`,
      });
    };

    detectCurrency();
  }, []);

  return currencyInfo;
};
