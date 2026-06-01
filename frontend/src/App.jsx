import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import {
  BarChart3, TrendingUp, DollarSign, Users, Bell, Search, Settings,
  ChevronDown, ChevronUp, Activity, Zap, Clock, ArrowUpRight,
  ArrowDownRight, Download, Filter, Plus, X, Check, AlertCircle,
  LayoutDashboard, LineChart as LineChartIcon, FileText, UserCircle, LogOut,
  Menu, RefreshCw, ShoppingCart, MessageSquare, Star,
  Layers, Box, Package, Sparkles
} from 'lucide-react';

const BASE = window.__BACKEND_URL__ || '';

async function apiFetch(path, opts = {}) {
  for (let i = 0; i < 5; i++) {
    try {
      const r = await fetch(BASE + path, opts);
      if (r.ok) return r.json();
    } catch (_) {}
    await new Promise(r => setTimeout(r, 1500));
  }
  return null;
}

const mockData = {
  kpis: [
    { label: 'Total Revenue', value: '$12,847', delta: 12.5, icon: DollarSign },
    { label: 'Active Users', value: '2,341', delta: 8.2, icon: Users },
    { label: 'Conversion Rate', value: '3.24%', delta: -2.1, icon: TrendingUp },
    { label: 'Avg. Session', value: '4m 32s', delta: 5.7, icon: Clock }
  ],
  chartData: [
    { day: 'Mon', value: 2400 }, { day: 'Tue', value: 3100 },
    { day: 'Wed', value: 2800 }, { day: 'Thu', value: 3600 },
    { day: 'Fri', value: 4200 }, { day: 'Sat', value: 3900 },
    { day: 'Sun', value: 4500 }
  ],
  activities: [
    { id: 1, user: 'Sarah Chen', action: 'Purchased Pro Plan', amount: '$29', time: '2 min ago', status: 'completed' },
    { id: 2, user: 'Mike Johnson', action: 'Upgraded to Team', amount: '$49', time: '15 min ago', status: 'completed' },
    { id: 3, user: 'Emily Davis', action: 'Cancelled Subscription', amount: '-$19', time: '1 hour ago', status: 'cancelled' },
    { id: 4, user: 'Alex Rivera', action: 'Trial Started', amount: '$0', time: '3 hours ago', status: 'active' },
    { id: 5, user: 'Lisa Wang', action: 'Payment Failed', amount: '$29', time: '5 hours ago', status: 'failed' }
  ],
  templates: [
    { name: 'Invoice Generator', price: '$9/mo', users: 847, rating: 4.8 },
    { name: 'Social Scheduler', price: '$19/mo', users: 623, rating: 4.6 },
    { name: 'Analytics Lite', price: '$14/mo', users: 511, rating: 4.7 },
    { name: 'Email Blaster', price: '$29/mo', users: 389, rating: 4.5 }
  ]
};

function CSSInjection() {
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = ':root { --accent: #00C9A7; --accent2: #1E3A5F; }';
      document.head.appendChild(style);
    return () => style.remove();
  }, []);
  return null;
}

function KPICard({ data, index }) {
  const [displayValue, setDisplayValue] = useState('');
  const { label, value, delta, icon: Icon } = data;
  const isPositive = delta >= 0;

  useEffect(() => {
    const num = parseFloat(value.replace(/[^0-9.]/g, ''));
    if (isNaN(num)) {
      setDisplayValue(value);
      return;
    }
    let current = 0;
    const steps = 20;
    const increment = num / steps;
    let step = 0;
    const timer = setInterval(() => {
      step++;
      if (step >= steps) {
        setDisplayValue(value);
        clearInterval(timer);
      } else {
        const formatted = value.includes('$') 
          ? `${Math.round(current).toLocaleString()}`
          : value.includes('%')
            ? `${(current).toFixed(2)}%`
            : Math.round(current).toLocaleString();
        setDisplayValue(formatted);
        current += increment;
      }
    }, 50);
    return () => clearInterval(timer);
  }, [value]);

  return (
    <div className="glass p-5 fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
      <div className="flex items-center justify-between mb-3">
        <div className="p-2 rounded-lg" style={{ backgroundColor: 'rgba(79, 70, 229, 0.1)' }}>
          <Icon className="w-5 h-5" style={{ color: '#4F46E5' }} />
        </div>
        <div className={`flex items-center gap-1 text-sm ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
          {isPositive ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
          <span>{Math.abs(delta)}%</span>
        </div>
      </div>
      <div className="text-2xl font-bold mb-1 count-animate">{displayValue}</div>
      <div className="text-sm text-slate-400">{label}</div>
    </div>
  );
}

function AreaChart({ data }) {
  const [animate, setAnimate] = useState(false);
  const svgRef = useRef(null);

  useEffect(() => {
    setAnimate(true);
  }, []);

  const width = 600;
  const height = 200;
  const padding = 40;
  const chartWidth = width - padding * 2;
  const chartHeight = height - padding * 2;

  const maxValue = Math.max(...(data || []).map(d => d.value));
  const minValue = 0;

  const points = (data || []).map((d, i) => ({
    x: padding + (i * chartWidth) / Math.max((data || []).length - 1, 1),
    y: padding + chartHeight - ((d.value - minValue) / (maxValue - minValue)) * chartHeight
  }));

  const areaPath = useMemo(() => {
    if (!points.length) return '';
    const p = points.map((pt, i) => `${i === 0 ? 'M' : 'L'}${pt.x},${pt.y}`).join(' ');
    return `${p} L${points[points.length - 1].x},${padding + chartHeight} L${points[0].x},${padding + chartHeight} Z`;
  }, [points]);

  const linePath = useMemo(() => {
    if (!points.length) return '';
    return points.map((pt, i) => `${i === 0 ? 'M' : 'L'}${pt.x},${pt.y}`).join(' ');
  }, [points]);

  return (
    <div className="glass p-5 fade-in">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold gradient-text">Weekly Revenue Trend</h3>
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <RefreshCw className="w-3 h-3" />
          <span>Last 7 days</span>
        </div>
      </div>
      <svg ref={svgRef} viewBox={`0 0 ${width} ${height}`} className="w-full" style={{ maxHeight: '200px' }}>
        <defs>
          <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#4F46E5" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#4F46E5" stopOpacity="0" />
          </linearGradient>
        </defs>
        {points.map((pt, i) => (
          <line key={i} x1={pt.x} y1={padding} x2={pt.x} y2={padding + chartHeight}
            stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
        ))}
        <path d={areaPath} fill="url(#areaGradient)" opacity={animate ? 1 : 0}
          style={{ transition: 'opacity 1s ease' }} />
        <path d={linePath} fill="none" stroke="#4F46E5" strokeWidth="2"
          strokeLinecap="round" strokeLinejoin="round"
          strokeDasharray={animate ? '1000' : '0'}
          strokeDashoffset={animate ? '0' : '1000'}
          style={{ transition: 'stroke-dashoffset 1.5s ease-in-out' }} />
        {points.map((pt, i) => (
          <circle key={i} cx={pt.x} cy={pt.y} r="3" fill="#4F46E5"
            className="hover:r-5" style={{ transition: 'all 0.2s' }} />
        ))}
        {(data || []).map((d, i) => (
          <text key={i} x={points[i]?.x || 0} y={height - 5}
            textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="10">
            {d.day}
          </text>
        ))}
      </svg>
    </div>
  );
}

function DataTable({ data, onSort, sortKey, sortDir }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredData, setFilteredData] = useState(data || []);

  useEffect(() => {
    let result = [...(data || [])];
    if (searchTerm) {
      result = result.filter(item =>
        item.user.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.action.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    if (sortKey) {
      result.sort((a, b) => {
        const aVal = a[sortKey];
        const bVal = b[sortKey];
        if (typeof aVal === 'string') {
          return sortDir === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        }
        return sortDir === 'asc' ? aVal - bVal : bVal - aVal;
      });
    }
    setFilteredData(result);
  }, [data, searchTerm, sortKey, sortDir]);

  const handleSort = useCallback((key) => {
    onSort(key);
  }, [onSort]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'text-emerald-400 bg-emerald-400/10';
      case 'cancelled': return 'text-red-400 bg-red-400/10';
      case 'active': return 'text-blue-400 bg-blue-400/10';
      case 'failed': return 'text-amber-400 bg-amber-400/10';
      default: return 'text-slate-400 bg-slate-400/10';
    }
  };

  return (
    <div className="glass p-5 fade-in">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Recent Activity</h3>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-white/5 border border-white/10 rounded-lg pl-9 pr-3 py-1.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 w-48"
            />
          </div>
          <button className="p-1.5 rounded-lg hover:bg-white/5 transition-all duration-200 text-slate-400 hover:text-slate-200">
            <Filter className="w-4 h-4" />
          </button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/5">
              <th className="text-left py-3 px-2 text-slate-400 font-medium cursor-pointer hover:text-slate-200"
                onClick={() => handleSort('user')}>
                <div className="flex items-center gap-1">
                  User
                  {sortKey === 'user' && (sortDir === 'asc' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />)}
                </div>
              </th>
              <th className="text-left py-3 px-2 text-slate-400 font-medium cursor-pointer hover:text-slate-200"
                onClick={() => handleSort('action')}>
                <div className="flex items-center gap-1">
                  Action
                  {sortKey === 'action' && (sortDir === 'asc' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />)}
                </div>
              </th>
              <th className="text-left py-3 px-2 text-slate-400 font-medium cursor-pointer hover:text-slate-200"
                onClick={() => handleSort('amount')}>
                <div className="flex items-center gap-1">
                  Amount
                  {sortKey === 'amount' && (sortDir === 'asc' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />)}
                </div>
              </th>
              <th className="text-left py-3 px-2 text-slate-400 font-medium cursor-pointer hover:text-slate-200"
                onClick={() => handleSort('time')}>
                <div className="flex items-center gap-1">
                  Time
                  {sortKey === 'time' && (sortDir === 'asc' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />)}
                </div>
              </th>
              <th className="text-left py-3 px-2 text-slate-400 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {(filteredData || []).map((row) => (
              <tr key={row.id} className="border-b border-white/5 hover:bg-white/5 transition-colors duration-150">
                <td className="py-3 px-2">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-full bg-indigo-500/20 flex items-center justify-center text-xs text-indigo-300">
                      {row.user.charAt(0)}
                    </div>
                    <span>{row.user}</span>
                  </div>
                </td>
                <td className="py-3 px-2">{row.action}</td>
                <td className="py-3 px-2 font-medium">{row.amount}</td>
                <td className="py-3 px-2 text-slate-400">{row.time}</td>
                <td className="py-3 px-2">
                  <span className={`px-2 py-0.5 rounded-full text-xs ${getStatusColor(row.status)}`}>
                    {row.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function QuickActions() {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', email: '', tool: '' });
  const [errors, setErrors] = useState({});
  const [toast, setToast] = useState(null);

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) newErrors.email = 'Invalid email';
    if (!formData.tool.trim()) newErrors.tool = 'Please select a tool';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    setToast({ type: 'success', message: 'Subscription request submitted successfully!' });
    setFormData({ name: '', email: '', tool: '' });
    setShowForm(false);
    setTimeout(() => setToast(null), 3000);
  };

  const actions = [
    { icon: Plus, label: 'New Template', color: 'bg-indigo-500/20 text-indigo-300' },
    { icon: Download, label: 'Export Data', color: 'bg-emerald-500/20 text-emerald-300' },
    { icon: MessageSquare, label: 'Send Update', color: 'bg-amber-500/20 text-amber-300' },
    { icon: Star, label: 'Top Tools', color: 'bg-pink-500/20 text-pink-300' }
  ];

  return (
    <div className="space-y-4">
      <div className="glass p-5 fade-in">
        <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
        <div className="space-y-2">
          {actions.map((action, i) => (
            <button key={i}
              onClick={() => {
                if (action.label === 'New Template') {
                  setShowForm(true);
                  setErrors({});
                }
              }}
              className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-white/5 transition-all duration-200 text-left">
              <div className={`p-2 rounded-lg ${action.color}`}>
                <action.icon className="w-4 h-4" />
              </div>
              <div>
                <div className="text-sm font-medium">{action.label}</div>
                <div className="text-xs text-slate-400 mt-0.5">Click to start</div>
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="glass p-5 fade-in">
        <h3 className="text-lg font-semibold mb-4">Popular Templates</h3>
        <div className="space-y-3">
          {(mockData.templates || []).map((template, i) => (
            <div key={i} className="flex items-center justify-between p-2 rounded-lg hover:bg-white/5 transition-colors">
              <div>
                <div className="text-sm font-medium">{template.name}</div>
                <div className="text-xs text-slate-400 mt-0.5">{template.users} users</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold" style={{ color: '#4F46E5' }}>{template.price}</div>
                <div className="flex items-center gap-1 text-xs text-amber-400">
                  <Star className="w-3 h-3 fill-current" />
                  {template.rating}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="glass p-6 w-96 fade-in">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">New Template Request</h3>
              <button onClick={() => setShowForm(false)} className="p-1 rounded-lg hover:bg-white/5 transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm text-slate-400 mb-1">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500/50"
                  placeholder="Your name"
                />
                {errors.name && <p className="text-xs text-red-400 mt-1">{errors.name}</p>}
              </div>
              <div>
                <label className="block text-sm text-slate-400 mb-1">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500/50"
                  placeholder="your@email.com"
                />
                {errors.email && <p className="text-xs text-red-400 mt-1">{errors.email}</p>}
              </div>
              <div>
                <label className="block text-sm text-slate-400 mb-1">Tool</label>
                <select
                  value={formData.tool}
                  onChange={(e) => setFormData(prev => ({ ...prev, tool: e.target.value }))}
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500/50"
                >
                  <option value="">Select a tool</option>
                  <option value="invoice">Invoice Generator</option>
                  <option value="social">Social Scheduler</option>
                  <option value="analytics">Analytics Lite</option>
                  <option value="email">Email Blaster</option>
                </select>
                {errors.tool && <p className="text-xs text-red-400 mt-1">{errors.tool}</p>}
              </div>
              <button
                type="submit"
                className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors duration-200"
              >
                Submit Request
              </button>
            </form>
          </div>
        </div>
      )}

      {toast && (
        <div className="fixed bottom-6 right-6 glass px-4 py-3 flex items-center gap-2 fade-in">
          <Check className="w-4 h-4 text-emerald-400" />
          <span className="text-sm">{toast.message}</span>
        </div>
      )}
    </div>
  );
}

function Sidebar() {
  const [activePage, setActivePage] = useState('dashboard');
  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', id: 'dashboard' },
    { icon: BarChart3, label: 'Analytics', id: 'analytics' },
    { icon: FileText, label: 'Reports', id: 'reports' },
    { icon: Settings, label: 'Settings', id: 'settings' }
  ];

  return (
    <aside className="w-64 flex-shrink-0 flex flex-col border-r border-white/5 bg-white/[0.02] h-full">
      <div className="p-6 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold gradient-text">SoloSuite</h1>
            <p className="text-xs text-slate-400">PixelForge Studios</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActivePage(item.id)}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all duration-200 ${
              activePage === item.id
                ? 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/20'
                : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
            }`}
          >
            <item.icon className="w-4 h-4" />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-4 border-t border-white/5">
        <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-slate-200 hover:bg-white/5 transition-all duration-200">
          <UserCircle className="w-4 h-4" />
          <span>Profile</span>
        </button>
        <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-red-400 hover:bg-red-500/5 transition-all duration-200">
          <LogOut className="w-4 h-4" />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}

function TopBar() {
  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-white/5 flex-shrink-0">
      <div className="flex items-center gap-4">
        <h2 className="text-sm font-semibold text-slate-300">Dashboard Overview</h2>
        <div className="flex items-center gap-1 text-xs text-slate-500">
          <span>Last updated:</span>
          <span>2 minutes ago</span>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <button className="p-2 rounded-lg hover:bg-white/5 transition-all duration-200 text-slate-400 hover:text-slate-200">
          <Bell className="w-4 h-4" />
        </button>
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-xs font-medium text-white">
          JD
        </div>
      </div>
    </header>
  );
}

export default function App() {
  const [kpiData, setKpiData] = useState(mockData.kpis);
  const [chartData, setChartData] = useState(mockData.chartData);
  const [activityData, setActivityData] = useState(mockData.activities);
  const [sortKey, setSortKey] = useState(null);
  const [sortDir, setSortDir] = useState('asc');
  const [loading, setLoading] = useState(true);

  const handleSort = useCallback((key) => {
    setSortKey(prevKey => {
      if (prevKey === key) {
        setSortDir(prev => prev === 'asc' ? 'desc' : 'asc');
        return key;
      }
      setSortDir('asc');
      return key;
    });
  }, []);

  useEffect(() => {
    async function fetchData() {
      const data = await apiFetch('/api/dashboard');
      if (data) {
        setKpiData(data.kpis || mockData.kpis);
        setChartData(data.chartData || mockData.chartData);
        setActivityData(data.activities || mockData.activities);
      }
      setLoading(false);
    }
    fetchData();
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-[#06080f] text-slate-100">
      <CSSInjection />
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
            {(kpiData || []).map((kpi, i) => (
              <KPICard key={i} data={kpi} index={i} />
            ))}
          </div>
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-6">
            <div className="xl:col-span-2">
              <AreaChart data={chartData} />
            </div>
            <div>
              <QuickActions />
            </div>
          </div>
          <DataTable
            data={activityData}
            onSort={handleSort}
            sortKey={sortKey}
            sortDir={sortDir}
          />
        </main>
      </div>
    </div>
  );
}