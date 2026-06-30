export const config = {
  matcher: '/:path*',
};

const USERNAME = process.env.BASIC_AUTH_USER ?? 'antigravity';
const PASSWORD = process.env.BASIC_AUTH_PASSWORD ?? 'Lx7XG$@KWWf!j%wt6xdA';

export default function middleware(request) {
  const authHeader = request.headers.get('authorization');

  if (authHeader) {
    const [scheme, encoded] = authHeader.split(' ');
    if (scheme === 'Basic' && encoded) {
      const decoded = atob(encoded);
      const i = decoded.indexOf(':');
      const user = decoded.slice(0, i);
      const pass = decoded.slice(i + 1);
      
      if (user === USERNAME && pass === PASSWORD) {
        return undefined;
      }
    }
  }

  return new Response('Authentication required.', {
    status: 401,
    headers: { 'WWW-Authenticate': 'Basic realm="Secure Area", charset="UTF-8"' },
  });
}