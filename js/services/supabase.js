import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL =
"https://ghlyavedvvblivlidlxg.supabase.co";

const SUPABASE_ANON_KEY =
"sb_publishable_-HIHdhPOjt_JxObSzIE7nQ_y21_r5fS";

export const supabase = createClient(
    SUPABASE_URL,
    SUPABASE_ANON_KEY
);