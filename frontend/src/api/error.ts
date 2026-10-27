import { isAxiosError } from "axios";

export interface ErrorMessageConfig {
  statusMessages?: Record<number, string>;
  defaultMessage: string;
}

export const getErrorMessage = (error: unknown, config: ErrorMessageConfig): string => {
  if (isAxiosError(error) && error.response?.status) {
    const status = error.response.status;
    
    if (config.statusMessages && config.statusMessages[status]) {
      return config.statusMessages[status];
    }
  }
  
  return config.defaultMessage;
}