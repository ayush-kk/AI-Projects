import { format, formatDistanceToNow } from 'date-fns';

export function formatDate(dateString) {
  return format(new Date(dateString), 'MMM d, yyyy h:mm a');
}

export function formatRelative(dateString) {
  return formatDistanceToNow(new Date(dateString), { addSuffix: true });
}

export function truncate(str, length = 50) {
  if (!str) return '';
  return str.length > length ? str.substring(0, length) + '...' : str;
}
