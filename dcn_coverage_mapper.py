
# src/store/authStore.ts
auth_store = """import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface User {
  id: string;
  email: string;
  name: string;
  credits: number;
  plan: string;
  referralCode: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string, referralCode?: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  updateCredits: (credits: number) => void;
}

const API_BASE = 'https://api.dcn.network/v1'; // Your backend URL

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isLoading: true,
  isAuthenticated: false,

  login: async (email, password) => {
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();
      if (!data.success) throw new Error(data.error);
      
      await AsyncStorage.setItem('token', data.data.accessToken);
      await AsyncStorage.setItem('refreshToken', data.data.refreshToken);
      
      set({
        user: data.data.user,
        token: data.data.accessToken,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      throw error;
    }
  },

  register: async (name, email, password, referralCode) => {
    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, referralCode }),
      });
      
      const data = await response.json();
      if (!data.success) throw new Error(data.error);
      
      await AsyncStorage.setItem('token', data.data.accessToken);
      await AsyncStorage.setItem('refreshToken', data.data.refreshToken);
      
      set({
        user: data.data.user,
        token: data.data.accessToken,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      throw error;
    }
  },

  logout: async () => {
    await AsyncStorage.multiRemove(['token', 'refreshToken']);
    set({ user: null, token: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    try {
      const token = await AsyncStorage.getItem('token');
      if (!token) {
        set({ isLoading: false, isAuthenticated: false });
        return;
      }
      
      // Validate token and get user data
      const response = await fetch(`${API_BASE}/users/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      
      const data = await response.json();
      if (data.success) {
        set({ user: data.data, token, isAuthenticated: true, isLoading: false });
      } else {
        await AsyncStorage.multiRemove(['token', 'refreshToken']);
        set({ isLoading: false, isAuthenticated: false });
      }
    } catch {
      set({ isLoading: false, isAuthenticated: false });
    }
  },

  updateCredits: (credits) => {
    set((state) => ({
      user: state.user ? { ...state.user, credits } : null,
    }));
  },
}));
"""

with open(f'{app_dir}/src/store/authStore.ts', 'w') as f:
    f.write(auth_store)

# src/store/sosStore.ts
sos_store = """import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Location from 'expo-location';
import * as Notifications from 'expo-notifications';
import { Vibration } from 'react-native';

interface EmergencyContact {
  id: string;
  name: string;
  phone: string;
  relationship: string;
}

interface SOSEvent {
  id: string;
  timestamp: number;
  location: { latitude: number; longitude: number } | null;
  status: 'triggered' | 'sent' | 'acknowledged' | 'resolved';
  contactsNotified: string[];
  meshRelays: number;
}

interface SOSState {
  isSOSEnabled: boolean;
  emergencyContacts: EmergencyContact[];
  sosHistory: SOSEvent[];
  isPanicking: boolean;
  
  initializeSOS: () => Promise<void>;
  triggerSOS: () => Promise<void>;
  addEmergencyContact: (contact: EmergencyContact) => Promise<void>;
  removeEmergencyContact: (id: string) => Promise<void>;
  resolveSOS: (eventId: string) => void;
  toggleSOSEnabled: (enabled: boolean) => Promise<void>;
}

export const useSOSStore = create<SOSState>((set, get) => ({
  isSOSEnabled: true,
  emergencyContacts: [],
  sosHistory: [],
  isPanicking: false,

  initializeSOS: async () => {
    try {
      const stored = await AsyncStorage.getItem('emergencyContacts');
      const enabled = await AsyncStorage.getItem('sosEnabled');
      const history = await AsyncStorage.getItem('sosHistory');
      
      set({
        emergencyContacts: stored ? JSON.parse(stored) : [],
        isSOSEnabled: enabled !== 'false',
        sosHistory: history ? JSON.parse(history) : [],
      });
    } catch (error) {
      console.error('SOS init error:', error);
    }
  },

  triggerSOS: async () => {
    const state = get();
    if (!state.isSOSEnabled || state.isPanicking) return;

    set({ isPanicking: true });
    
    // Vibrate pattern: SOS in Morse (... --- ...)
    Vibration.vibrate([200, 100, 200, 100, 200, 300, 600, 100, 600, 100, 600, 300, 200, 100, 200, 100, 200], true);

    try {
      // Get location
      const location = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.Highest,
      });

      const sosEvent: SOSEvent = {
        id: Date.now().toString(),
        timestamp: Date.now(),
        location: {
          latitude: location.coords.latitude,
          longitude: location.coords.longitude,
        },
        status: 'triggered',
        contactsNotified: [],
        meshRelays: 0,
      };

      // Send notifications to emergency contacts
      for (const contact of state.emergencyContacts) {
        try {
          // Send SMS via backend
          await sendEmergencySMS(contact.phone, sosEvent);
          sosEvent.contactsNotified.push(contact.phone);
        } catch (err) {
          console.error(`Failed to notify ${contact.name}:`, err);
        }
      }

      // Send local notification
      await Notifications.scheduleNotificationAsync({
        content: {
          title: '🚨 SOS ALERT ACTIVATED',
          body: `Location shared with ${sosEvent.contactsNotified.length} contacts`,
          sound: 'sos_alarm.wav',
          priority: Notifications.AndroidImportance.MAX,
        },
        trigger: null,
      });

      sosEvent.status = 'sent';
      
      const updatedHistory = [sosEvent, ...state.sosHistory];
      await AsyncStorage.setItem('sosHistory', JSON.stringify(updatedHistory));
      
      set({ sosHistory: updatedHistory, isPanicking: false });
      
      // Stop vibration after 10 seconds
      setTimeout(() => Vibration.cancel(), 10000);
      
    } catch (error) {
      console.error('SOS trigger error:', error);
      set({ isPanicking: false });
      Vibration.cancel();
    }
  },

  addEmergencyContact: async (contact) => {
    const state = get();
    const updated = [...state.emergencyContacts, contact];
    await AsyncStorage.setItem('emergencyContacts', JSON.stringify(updated));
    set({ emergencyContacts: updated });
  },

  removeEmergencyContact: async (id) => {
    const state = get();
    const updated = state.emergencyContacts.filter(c => c.id !== id);
    await AsyncStorage.setItem('emergencyContacts', JSON.stringify(updated));
    set({ emergencyContacts: updated });
  },

  resolveSOS: (eventId) => {
    set((state) => ({
      sosHistory: state.sosHistory.map(event =>
        event.id === eventId ? { ...event, status: 'resolved' as const } : event
      ),
    }));
  },

  toggleSOSEnabled: async (enabled) => {
    await AsyncStorage.setItem('sosEnabled', String(enabled));
    set({ isSOSEnabled: enabled });
  },
}));

async function sendEmergencySMS(phone: string, event: SOSEvent) {
  // This would call your backend API to send SMS
  // For now, placeholder
  console.log(`Sending SOS to ${phone}:`, event.location);
}
"""

with open(f'{app_dir}/src/store/sosStore.ts', 'w') as f:
    f.write(sos_store)

# src/store/dataStore.ts
data_store = """import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface DataPlan {
  id: string;
  name: string;
  dataMB: number;
  price: number;
  currency: string;
  duration: string;
  features: string[];
}

interface DataUsage {
  date: string;
  usedMB: number;
  appBreakdown: { app: string; usedMB: number }[];
}

interface DataState {
  currentPlan: DataPlan | null;
  remainingMB: number;
  totalMB: number;
  usageHistory: DataUsage[];
  isOffline: boolean;
  
  loadDataPlan: () => Promise<void>;
  useData: (mb: number, app: string) => void;
  purchasePlan: (plan: DataPlan) => Promise<void>;
  setOfflineMode: (offline: boolean) => void;
}

export const useDataStore = create<DataState>((set, get) => ({
  currentPlan: null,
  remainingMB: 0,
  totalMB: 0,
  usageHistory: [],
  isOffline: false,

  loadDataPlan: async () => {
    try {
      const plan = await AsyncStorage.getItem('currentPlan');
      const remaining = await AsyncStorage.getItem('remainingMB');
      const history = await AsyncStorage.getItem('usageHistory');
      
      set({
        currentPlan: plan ? JSON.parse(plan) : null,
        remainingMB: remaining ? parseInt(remaining) : 0,
        totalMB: plan ? JSON.parse(plan).dataMB : 0,
        usageHistory: history ? JSON.parse(history) : [],
      });
    } catch (error) {
      console.error('Data plan load error:', error);
    }
  },

  useData: (mb, app) => {
    set((state) => {
      const newRemaining = Math.max(0, state.remainingMB - mb);
      const today = new Date().toISOString().split('T')[0];
      
      const updatedHistory = [...state.usageHistory];
      const todayIndex = updatedHistory.findIndex(u => u.date === today);
      
      if (todayIndex >= 0) {
        updatedHistory[todayIndex].usedMB += mb;
        const appIndex = updatedHistory[todayIndex].appBreakdown.findIndex(a => a.app === app);
        if (appIndex >= 0) {
          updatedHistory[todayIndex].appBreakdown[appIndex].usedMB += mb;
        } else {
          updatedHistory[todayIndex].appBreakdown.push({ app, usedMB: mb });
        }
      } else {
        updatedHistory.unshift({
          date: today,
          usedMB: mb,
          appBreakdown: [{ app, usedMB: mb }],
        });
      }
      
      AsyncStorage.setItem('remainingMB', String(newRemaining));
      AsyncStorage.setItem('usageHistory', JSON.stringify(updatedHistory));
      
      return { remainingMB: newRemaining, usageHistory: updatedHistory };
    });
  },

  purchasePlan: async (plan) => {
    await AsyncStorage.setItem('currentPlan', JSON.stringify(plan));
    await AsyncStorage.setItem('remainingMB', String(plan.dataMB));
    set({
      currentPlan: plan,
      remainingMB: plan.dataMB,
      totalMB: plan.dataMB,
    });
  },

  setOfflineMode: (offline) => set({ isOffline: offline }),
}));
"""

with open(f'{app_dir}/src/store/dataStore.ts', 'w') as f:
    f.write(data_store)

print("Store files created")
