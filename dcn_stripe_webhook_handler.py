
# src/screens/ProfileScreen.tsx
profile_screen = """import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import { useAuthStore } from '../store/authStore';
import { useSOSStore } from '../store/sosStore';

interface MenuItem {
  icon: keyof typeof Ionicons.glyphMap;
  label: string;
  value?: string;
  onPress?: () => void;
  hasSwitch?: boolean;
  switchValue?: boolean;
  onSwitchChange?: (value: boolean) => void;
  danger?: boolean;
}

export default function ProfileScreen() {
  const { user, logout } = useAuthStore();
  const { isSOSEnabled, toggleSOSEnabled } = useSOSStore();

  const menuItems: MenuItem[] = [
    {
      icon: 'person-outline',
      label: 'Edit Profile',
      onPress: () => {},
    },
    {
      icon: 'shield-checkmark-outline',
      label: 'Emergency Contacts',
      value: `${user?.credits || 0} set`,
      onPress: () => {},
    },
    {
      icon: 'notifications-outline',
      label: 'Push Notifications',
      hasSwitch: true,
      switchValue: true,
      onSwitchChange: () => {},
    },
    {
      icon: 'alert-circle-outline',
      label: 'SOS Enabled',
      hasSwitch: true,
      switchValue: isSOSEnabled,
      onSwitchChange: toggleSOSEnabled,
    },
    {
      icon: 'moon-outline',
      label: 'Dark Mode',
      value: 'System',
      onPress: () => {},
    },
    {
      icon: 'globe-outline',
      label: 'Language',
      value: 'English',
      onPress: () => {},
    },
    {
      icon: 'help-circle-outline',
      label: 'Help & Support',
      onPress: () => {},
    },
    {
      icon: 'document-text-outline',
      label: 'Privacy Policy',
      onPress: () => {},
    },
    {
      icon: 'log-out-outline',
      label: 'Logout',
      danger: true,
      onPress: logout,
    },
  ];

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Profile Header */}
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {user?.name?.charAt(0).toUpperCase() || 'U'}
          </Text>
        </View>
        <Text style={styles.name}>{user?.name || 'User'}</Text>
        <Text style={styles.email}>{user?.email || 'user@dcn.ai'}</Text>
        
        <View style={styles.planBadge}>
          <Text style={styles.planText}>{(user?.plan || 'Free').toUpperCase()}</Text>
        </View>
      </View>

      {/* Stats */}
      <View style={styles.statsContainer}>
        <View style={styles.statBox}>
          <Text style={styles.statNumber}>{user?.credits || 0}</Text>
          <Text style={styles.statLabel}>Credits</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statBox}>
          <Text style={styles.statNumber}>{user?.totalVideosGenerated || 0}</Text>
          <Text style={styles.statLabel}>Videos</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statBox}>
          <Text style={styles.statNumber}>0</Text>
          <Text style={styles.statLabel}>Referrals</Text>
        </View>
      </View>

      {/* Referral Code */}
      <View style={styles.referralCard}>
        <View style={styles.referralContent}>
          <Ionicons name="gift-outline" size={24} color="#00e676" />
          <View style={styles.referralText}>
            <Text style={styles.referralTitle}>Your Referral Code</Text>
            <Text style={styles.referralCode}>{user?.referralCode || 'DCNXXXX'}</Text>
          </View>
        </View>
        <TouchableOpacity style={styles.copyButton}>
          <Ionicons name="copy-outline" size={18} color="#d4a853" />
        </TouchableOpacity>
      </View>

      {/* Menu */}
      <View style={styles.menuSection}>
        <Text style={styles.menuTitle}>Settings</Text>
        {menuItems.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={[
              styles.menuItem,
              index === menuItems.length - 1 && styles.menuItemLast,
            ]}
            onPress={item.onPress}
            activeOpacity={0.7}
          >
            <View style={styles.menuItemLeft}>
              <Ionicons
                name={item.icon}
                size={22}
                color={item.danger ? '#ff3d3d' : '#8a9ab0'}
              />
              <Text style={[
                styles.menuItemLabel,
                item.danger && styles.menuItemLabelDanger,
              ]}>
                {item.label}
              </Text>
            </View>
            <View style={styles.menuItemRight}>
              {item.value && (
                <Text style={styles.menuItemValue}>{item.value}</Text>
              )}
              {item.hasSwitch ? (
                <Switch
                  value={item.switchValue}
                  onValueChange={item.onSwitchChange}
                  trackColor={{ false: '#4a5a70', true: 'rgba(212,168,83,0.3)' }}
                  thumbColor={item.switchValue ? '#d4a853' : '#8a9ab0'}
                />
              ) : (
                !item.danger && (
                  <Ionicons name="chevron-forward" size={18} color="#4a5a70" />
                )
              )}
            </View>
          </TouchableOpacity>
        ))}
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>DCN App v1.0.0</Text>
        <Text style={styles.footerSubtext}>© 2026 DCN — The Network of the Future</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050a14',
    paddingTop: 60,
  },
  header: {
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingBottom: 24,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(212,168,83,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: 'rgba(212,168,83,0.3)',
  },
  avatarText: {
    color: '#d4a853',
    fontSize: 32,
    fontWeight: '800',
  },
  name: {
    color: '#f0f4f8',
    fontSize: 20,
    fontWeight: '700',
    marginTop: 12,
  },
  email: {
    color: '#8a9ab0',
    fontSize: 14,
    marginTop: 4,
  },
  planBadge: {
    marginTop: 12,
    paddingHorizontal: 16,
    paddingVertical: 6,
    backgroundColor: 'rgba(212,168,83,0.15)',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(212,168,83,0.25)',
  },
  planText: {
    color: '#d4a853',
    fontWeight: '700',
    fontSize: 12,
    letterSpacing: 1,
  },
  statsContainer: {
    flexDirection: 'row',
    marginHorizontal: 20,
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  statBox: {
    flex: 1,
    alignItems: 'center',
  },
  statDivider: {
    width: 1,
    backgroundColor: 'rgba(255,255,255,0.06)',
  },
  statNumber: {
    color: '#f0f4f8',
    fontSize: 24,
    fontWeight: '800',
  },
  statLabel: {
    color: '#8a9ab0',
    fontSize: 12,
    marginTop: 4,
  },
  referralCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginHorizontal: 20,
    marginTop: 16,
    backgroundColor: 'rgba(0,230,118,0.08)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(0,230,118,0.15)',
  },
  referralContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  referralText: {
    gap: 2,
  },
  referralTitle: {
    color: '#8a9ab0',
    fontSize: 12,
  },
  referralCode: {
    color: '#00e676',
    fontSize: 16,
    fontWeight: '800',
    letterSpacing: 1,
  },
  copyButton: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: 'rgba(212,168,83,0.15)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  menuSection: {
    marginTop: 24,
    paddingHorizontal: 20,
  },
  menuTitle: {
    color: '#8a9ab0',
    fontSize: 13,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 12,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.04)',
  },
  menuItemLast: {
    borderBottomWidth: 0,
  },
  menuItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
  },
  menuItemLabel: {
    color: '#f0f4f8',
    fontSize: 15,
    fontWeight: '500',
  },
  menuItemLabelDanger: {
    color: '#ff3d3d',
  },
  menuItemRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  menuItemValue: {
    color: '#4a5a70',
    fontSize: 14,
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 32,
    gap: 4,
  },
  footerText: {
    color: '#4a5a70',
    fontSize: 13,
  },
  footerSubtext: {
    color: '#4a5a70',
    fontSize: 11,
  },
});
"""

with open(f'{app_dir}/src/screens/ProfileScreen.tsx', 'w') as f:
    f.write(profile_screen)

# src/screens/LoginScreen.tsx
login_screen = """import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

import { useAuthStore } from '../store/authStore';

export default function LoginScreen() {
  const navigation = useNavigation();
  const { login } = useAuthStore();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <View style={styles.content}>
        {/* Logo */}
        <View style={styles.logoContainer}>
          <LinearGradient
            colors={['#d4a853', '#00e5ff']}
            style={styles.logo}
          >
            <Text style={styles.logoText}>D</Text>
          </LinearGradient>
          <Text style={styles.brandName}>DCN <Text style={styles.brandHighlight}>Network</Text></Text>
          <Text style={styles.tagline}>The Network of the Future</Text>
        </View>

        {/* Form */}
        <View style={styles.form}>
          {error ? (
            <View style={styles.errorContainer}>
              <Ionicons name="alert-circle" size={16} color="#ff3d3d" />
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          <View style={styles.inputContainer}>
            <Ionicons name="mail-outline" size={20} color="#4a5a70" />
            <TextInput
              style={styles.input}
              placeholder="Email address"
              placeholderTextColor="#4a5a70"
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              keyboardType="email-address"
            />
          </View>

          <View style={styles.inputContainer}>
            <Ionicons name="lock-closed-outline" size={20} color="#4a5a70" />
            <TextInput
              style={styles.input}
              placeholder="Password"
              placeholderTextColor="#4a5a70"
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
            />
            <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
              <Ionicons
                name={showPassword ? 'eye-off-outline' : 'eye-outline'}
                size={20}
                color="#4a5a70"
              />
            </TouchableOpacity>
          </View>

          <TouchableOpacity style={styles.forgotPassword}>
            <Text style={styles.forgotPasswordText}>Forgot password?</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.loginButton}
            onPress={handleLogin}
            disabled={isLoading}
            activeOpacity={0.8}
          >
            <LinearGradient
              colors={['#d4a853', '#f0c96a']}
              style={styles.loginGradient}
            >
              {isLoading ? (
                <ActivityIndicator color="#050a14" />
              ) : (
                <Text style={styles.loginButtonText}>Sign In</Text>
              )}
            </LinearGradient>
          </TouchableOpacity>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>Don't have an account?</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Register' as never)}>
            <Text style={styles.footerLink}>Create Account</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050a14',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 32,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 48,
  },
  logo: {
    width: 72,
    height: 72,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  logoText: {
    fontSize: 32,
    fontWeight: '900',
    color: '#050a14',
  },
  brandName: {
    fontSize: 24,
    fontWeight: '800',
    color: '#f0f4f8',
  },
  brandHighlight: {
    color: '#d4a853',
  },
  tagline: {
    color: '#4a5a70',
    fontSize: 14,
    marginTop: 8,
  },
  form: {
    gap: 16,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: 'rgba(255,61,61,0.1)',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(255,61,61,0.2)',
  },
  errorText: {
    color: '#ff3d3d',
    fontSize: 13,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(10,20,40,0.8)',
    borderRadius: 14,
    paddingHorizontal: 16,
    height: 56,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
    gap: 12,
  },
  input: {
    flex: 1,
    color: '#f0f4f8',
    fontSize: 15,
  },
  forgotPassword: {
    alignSelf: 'flex-end',
  },
  forgotPasswordText: {
    color: '#d4a853',
    fontSize: 13,
    fontWeight: '600',
  },
  loginButton: {
    borderRadius: 14,
    overflow: 'hidden',
    marginTop: 8,
  },
  loginGradient: {
    height: 56,
    alignItems: 'center',
    justifyContent: 'center',
  },
  loginButtonText: {
    color: '#050a14',
    fontSize: 16,
    fontWeight: '800',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 6,
    marginTop: 32,
  },
  footerText: {
    color: '#8a9ab0',
    fontSize: 14,
  },
  footerLink: {
    color: '#d4a853',
    fontSize: 14,
    fontWeight: '700',
  },
});
"""

with open(f'{app_dir}/src/screens/LoginScreen.tsx', 'w') as f:
    f.write(login_screen)

print("ProfileScreen and LoginScreen created")
