const API_BASE = '/api/v1';
const WS_BASE = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/api/v1`;

export { API_BASE, WS_BASE };
