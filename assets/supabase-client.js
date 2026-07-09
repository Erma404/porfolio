import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// Clé publishable : safe à exposer côté client par design, la sécurité vient de RLS.
const SUPABASE_URL = 'https://zgrssodquslflvkzxcji.supabase.co';
const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_Ji5XFUeJeNrmEerUdgmsvA_LfR380Yk';
const FUNCTIONS_URL = `${SUPABASE_URL}/functions/v1`;

export const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);

export async function requireSession(redirectTo) {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session) {
    window.location.href = redirectTo;
    return null;
  }
  return session;
}

export async function requireAdminSession() {
  const session = await requireSession('/admin/');
  if (!session) return null;
  if (session.user.email !== 'ernestinemtb@gmail.com') {
    await supabase.auth.signOut();
    window.location.href = '/admin/';
    return null;
  }
  return session;
}

export async function callFunction(name, body) {
  const { data: { session } } = await supabase.auth.getSession();
  const res = await fetch(`${FUNCTIONS_URL}/${name}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      apikey: SUPABASE_PUBLISHABLE_KEY,
      Authorization: `Bearer ${session?.access_token || SUPABASE_PUBLISHABLE_KEY}`,
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok || data.error) {
    throw new Error(data.message || 'Erreur serveur');
  }
  return data;
}
