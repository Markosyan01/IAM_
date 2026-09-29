import { createContext, useContext, useEffect, useState } from "react";
import { Routes, Route, Link, NavLink, useParams, useNavigate } from "react-router-dom";
import { api, token } from "./api.js";
import { LANGS, UI } from "./i18n.js";

const Ctx = createContext(null);
const useApp = () => useContext(Ctx);

const HERO_IMG =
  "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1000&q=70";

function Photo({ src, alt = "", className = "" }) {
  const [broken, setBroken] = useState(false);
  if (broken || !src) return <div className={`photo fallback ${className}`} aria-hidden="true" />;
  return <img className={`photo ${className}`} src={src} alt={alt} loading="lazy" onError={() => setBroken(true)} />;
}

function useLoad(path, deps) {
  const [state, setState] = useState({ data: null, error: null });
  useEffect(() => {
    let live = true;
    setState({ data: null, error: null });
    api(path)
      .then((data) => live && setState({ data, error: null }))
      .catch((error) => live && setState({ data: null, error }));
    return () => { live = false; };
    // eslint-disable-next-line
  }, deps);
  return state;
}

function Header() {
  const { lang, setLang, t, user, logout } = useApp();
  return (
    <header className="bar">
      <Link to="/" className="brand">CodeLab</Link>
      <nav className="nav">
        <NavLink to="/" end>{t.courses}</NavLink>
        {user && <NavLink to="/progress">{t.myProgress}</NavLink>}
      </nav>
      <div className="langs" role="group" aria-label="Language">
        {LANGS.map((l) => (
          <button key={l.code} className={l.code === lang ? "on" : ""} onClick={() => setLang(l.code)}>
            {l.label}
          </button>
        ))}
      </div>
      <div className="acct">
        {user ? (
          <>
            <span className="who">{user.name}</span>
            <button className="btn ghost" onClick={logout}>{t.logout}</button>
          </>
        ) : (
          <>
            <Link className="btn ghost" to="/login">{t.login}</Link>
            <Link className="btn" to="/register">{t.register}</Link>
          </>
        )}
      </div>
    </header>
  );
}

function CourseCard({ c }) {
  const { t } = useApp();
  const pct = c.lesson_count ? Math.round((c.done / c.lesson_count) * 100) : 0;
  return (
    <Link to={`/courses/${c.slug}`} className="card">
      <Photo src={c.image} alt={c.title} />
      <div className="card-body">
        <span className={`tag ${c.level}`}>{t[c.level]}</span>
        <h3>{c.title}</h3>
        <p>{c.description}</p>
        <div className="meta">
          <span>{c.lesson_count} {t.lessons.toLowerCase()}</span>
          {c.done > 0 && <span>{pct}% {t.completed}</span>}
        </div>
        {c.done > 0 && <div className="meter"><i style={{ width: `${pct}%` }} /></div>}
      </div>
    </Link>
  );
}

function Home() {
  const { lang, t, user } = useApp();
  const { data } = useLoad(`/courses?lang=${lang}`, [lang, user?.email]);
  return (
    <>
      <section className="hero">
        <div>
          <h1>{t.heroTitle}</h1>
          <p>{t.heroText}</p>
          <a className="btn big" href="#courses">{t.browse}</a>
        </div>
        <div className="hero-photo"><Photo src={HERO_IMG} alt="" /></div>
      </section>
      <section id="courses" className="wrap">
        <h2>{t.courses}</h2>
        {!data ? <p className="muted">{t.loading}</p> : <div className="grid">{data.map((c) => <CourseCard key={c.slug} c={c} />)}</div>}
      </section>
    </>
  );
}

function Course() {
  const { slug } = useParams();
  const { lang, t, user } = useApp();
  const { data, error } = useLoad(`/courses/${slug}?lang=${lang}`, [slug, lang, user?.email]);
  if (error) return <p className="wrap">{t.notFound}</p>;
  if (!data) return <p className="wrap muted">{t.loading}</p>;
  return (
    <div className="wrap narrow">
      <Link to="/" className="back">{t.back}</Link>
      <Photo className="banner" src={data.image} alt={data.title} />
      <span className={`tag ${data.level}`}>{t[data.level]}</span>
      <h1>{data.title}</h1>
      <p className="lead">{data.description}</p>
      {!user && <p className="notice">{t.loginNeeded}</p>}
      <h2>{t.lessons}</h2>
      <ol className="lesson-list">
        {data.lessons.map((l) => (
          <li key={l.id}>
            <Link to={`/lessons/${l.id}`}>
              <span className={`tick ${l.done ? "on" : ""}`}>{l.done ? "✓" : l.position}</span>
              <span>{l.title}</span>
            </Link>
          </li>
        ))}
      </ol>
    </div>
  );
}

function Lesson() {
  const { id } = useParams();
  const { lang, t, user } = useApp();
  const navigate = useNavigate();
  const { data, error } = useLoad(`/lessons/${id}?lang=${lang}`, [id, lang, user?.email]);
  const [done, setDone] = useState(false);
  useEffect(() => { if (data) setDone(data.done); }, [data]);
  if (error) return <p className="wrap">{t.notFound}</p>;
  if (!data) return <p className="wrap muted">{t.loading}</p>;

  const toggle = async () => {
    if (!user) return navigate("/login");
    await api(`/lessons/${data.id}/complete`, { method: done ? "DELETE" : "POST" });
    setDone(!done);
  };

  return (
    <article className="wrap narrow">
      <Link to={`/courses/${data.course_slug}`} className="back">{data.course_title}</Link>
      <h1>{data.title}</h1>
      <p className="lead">{data.body}</p>
      <pre className="code"><code>{data.code}</code></pre>
      <div className="row">
        <button className={`btn ${done ? "ghost" : ""}`} onClick={toggle}>
          {done ? `✓ ${t.done} · ${t.undo}` : t.markDone}
        </button>
        {!user && <span className="muted">{t.loginNeeded}</span>}
      </div>
      <div className="row split">
        {data.prev_id ? <Link className="btn ghost" to={`/lessons/${data.prev_id}`}>{t.prev}</Link> : <span />}
        {data.next_id && <Link className="btn" to={`/lessons/${data.next_id}`}>{t.next}</Link>}
      </div>
    </article>
  );
}

function Auth({ mode }) {
  const { t, setSession } = useApp();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const body = mode === "login" ? { email: form.email, password: form.password } : form;
      const res = await api(`/auth/${mode}`, { method: "POST", body });
      setSession(res.token, res.user);
      navigate("/");
    } catch (err) {
      setError(t[`err_${err.message}`] || t.err_generic);
    }
  };

  return (
    <div className="wrap tiny">
      <h1>{mode === "login" ? t.login : t.register}</h1>
      <div className="form" role="form">
        {mode === "register" && (
          <label>{t.name}<input value={form.name} onChange={set("name")} autoComplete="name" /></label>
        )}
        <label>{t.email}<input type="email" value={form.email} onChange={set("email")} autoComplete="email" /></label>
        <label>{t.password}<input type="password" value={form.password} onChange={set("password")}
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          onKeyDown={(e) => e.key === "Enter" && submit(e)} /></label>
        {error && <p className="error" role="alert">{error}</p>}
        <button className="btn big" onClick={submit}>{mode === "login" ? t.login : t.register}</button>
      </div>
      <p className="muted">
        {mode === "login" ? t.noAccount : t.haveAccount}{" "}
        <Link to={mode === "login" ? "/register" : "/login"}>{mode === "login" ? t.register : t.login}</Link>
      </p>
    </div>
  );
}

function Progress() {
  const { lang, t, user } = useApp();
  const { data } = useLoad(`/courses?lang=${lang}`, [lang, user?.email]);
  if (!user) return <p className="wrap">{t.loginNeeded}</p>;
  if (!data) return <p className="wrap muted">{t.loading}</p>;
  return (
    <div className="wrap narrow">
      <h1>{t.myProgress}</h1>
      {data.map((c) => {
        const pct = c.lesson_count ? Math.round((c.done / c.lesson_count) * 100) : 0;
        return (
          <Link key={c.slug} to={`/courses/${c.slug}`} className="prog">
            <strong>{c.title}</strong>
            <span>{c.done}/{c.lesson_count} {t.completed}</span>
            <div className="meter"><i style={{ width: `${pct}%` }} /></div>
          </Link>
        );
      })}
    </div>
  );
}

export default function App() {
  const [lang, setLangState] = useState(localStorage.getItem("codelab_lang") || "en");
  const [user, setUser] = useState(null);

  const setLang = (l) => { localStorage.setItem("codelab_lang", l); setLangState(l); };
  useEffect(() => { document.documentElement.lang = lang; }, [lang]);
  useEffect(() => {
    if (token.get()) api("/me").then(setUser).catch(() => token.clear());
  }, []);

  const setSession = (tk, u) => { token.set(tk); setUser(u); };
  const logout = () => { token.clear(); setUser(null); };
  const t = UI[lang];

  return (
    <Ctx.Provider value={{ lang, setLang, t, user, setSession, logout }}>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/courses/:slug" element={<Course />} />
          <Route path="/lessons/:id" element={<Lesson />} />
          <Route path="/login" element={<Auth mode="login" />} />
          <Route path="/register" element={<Auth mode="register" />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="*" element={<p className="wrap">{t.notFound}</p>} />
        </Routes>
      </main>
      <footer className="foot">{t.footer}</footer>
    </Ctx.Provider>
  );
}
