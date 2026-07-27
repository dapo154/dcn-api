
# src/screens/DataScreen.tsx
data_screen = """import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

import { useDataStore } from '../store/dataStore';
import { useAuthStore } from '../store/authStore';

const { width } = Dimensions.get('window');

const DATA_PLANS = [
  {
    id: 'basic',
    name: 'Basic',
    dataGB: 5,
    price: 500, // NGN
    duration: '30 days',
    features: ['5GB Data', 'Standard Speed', '1 Device'],
    color: ['#00e5ff', '#00b8d4'],
  },
  {
    id: 'standard',
    name: 'Standard',
    dataGB: 20,
    price: 1500,
    duration: '30 days',
    features: ['20GB Data', 'High Speed', '3 Devices', 'SOS Priority'],
    color: ['#d4a853', '#f0c96a'],
    popular: true,
  },
  {
    id: 'premium',
    name: 'Premium',
    dataGB: 100,
    price: 5000,
    duration: '30 days',
    features: ['100GB Data', 'Ultra Speed', '5 Devices', 'SOS Priority', 'Mesh Network'],
    color: ['#00e676', '#00c853'],
  },
];

export default function DataScreen() {
  const navigation = useNavigation();
  const { currentPlan, remainingMB, totalMB, usageHistory, loadDataPlan } = useDataStore();
  const { user } = useAuthStore();

  useEffect(() => {
    loadDataPlan();
  }, []);

  const dataPercentage = totalMB > 0 ? (remainingMB / totalMB) * 100 : 0;
  const todayUsage = usageHistory[0]?.usedMB || 0;

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>My Data</Text>
      </View>

      {/* Current Plan Card */}
      <View style={styles.planCard}>
        <LinearGradient
          colors={['rgba(212,168,83,0.15)', 'rgba(0,229,255,0.05)']}
          style={styles.planGradient}
        >
          <View style={styles.planInfo}>
            <Text style={styles.planLabel}>Current Plan</Text>
            <Text style={styles.planName}>{currentPlan?.name || 'Free'}</Text>
            <Text style={styles.planExpiry}>
              {currentPlan ? `Expires in ${currentPlan.duration}` : 'No active plan'}
            </Text>
          </View>
          
          <View style={styles.dataCircle}>
            <Text style={styles.dataPercent}>{Math.round(dataPercentage)}%</Text>
            <Text style={styles.dataRemaining}>
              {remainingMB >= 1024 
                ? `${(remainingMB / 1024).toFixed(1)}GB` 
                : `${remainingMB}MB`}
            </Text>
          </View>
        </LinearGradient>

        {/* Progress Bar */}
        <View style={styles.progressSection}>
          <View style={styles.progressBackground}>
            <View 
              style={[
                styles.progressFill, 
                { width: `${dataPercentage}%` },
                dataPercentage < 20 && styles.progressFillLow,
              ]} 
            />
          </View>
          <View style={styles.progressLabels}>
            <Text style={styles.progressLabel}>Used</Text>
            <Text style={styles.progressLabel}>
              {totalMB >= 1024 ? `${(totalMB / 1024).toFixed(1)}GB` : `${totalMB}MB`} Total
            </Text>
          </View>
        </View>
      </View>

      {/* Usage Stats */}
      <View style={styles.statsCard}>
        <Text style={styles.statsTitle}>Today's Usage</Text>
        <View style={styles.statsGrid}>
          <View style={styles.statItem}>
            <Ionicons name="phone-portrait" size={20} color="#00e5ff" />
            <Text style={styles.statValue}>
              {todayUsage >= 1024 
                ? `${(todayUsage / 1024).toFixed(1)} GB` 
                : `${todayUsage} MB`}
            </Text>
            <Text style={styles.statLabel}>Total Used</Text>
          </View>
          <View style={styles.statItem}>
            <Ionicons name="time" size={20} color="#d4a853" />
            <Text style={styles.statValue}>4h 32m</Text>
            <Text style={styles.statLabel}>Online Time</Text>
          </View>
          <View style={styles.statItem}>
            <Ionicons name="speedometer" size={20} color="#00e676" />
            <Text style={styles.statValue}>24 Mbps</Text>
            <Text style={styles.statLabel}>Avg Speed</Text>
          </View>
        </View>
      </View>

      {/* Data Plans */}
      <View style={styles.plansSection}>
        <Text style={styles.plansTitle}>Data Plans</Text>
        {DATA_PLANS.map((plan) => (
          <TouchableOpacity
            key={plan.id}
            style={[
              styles.planOption,
              plan.popular && styles.planOptionPopular,
            ]}
            onPress={() => navigation.navigate('DataPlans' as never)}
            activeOpacity={0.8}
          >
            <LinearGradient
              colors={plan.color.map(c => c + '20') as [string, string]}
              style={styles.planOptionGradient}
            >
              {plan.popular && (
                <View style={styles.popularBadge}>
                  <Text style={styles.popularText}>POPULAR</Text>
                </View>
              )}
              <View style={styles.planOptionHeader}>
                <View>
                  <Text style={styles.planOptionName}>{plan.name}</Text>
                  <Text style={styles.planOptionData}>{plan.dataGB}GB</Text>
                </View>
                <View style={styles.planOptionPrice}>
                  <Text style={styles.priceCurrency}>₦</Text>
                  <Text style={styles.priceAmount}>{plan.price.toLocaleString()}</Text>
                </View>
              </View>
              <View style={styles.planFeatures}>
                {plan.features.map((feature, idx) => (
                  <View key={idx} style={styles.featureItem}>
                    <Ionicons name="checkmark-circle" size={14} color={plan.color[0]} />
                    <Text style={styles.featureText}>{feature}</Text>
                  </View>
                ))}
              </View>
            </LinearGradient>
          </TouchableOpacity>
        ))}
      </View>

      {/* Referral Banner */}
      <TouchableOpacity style={styles.referralBanner}>
        <LinearGradient
          colors={['rgba(0,230,118,0.15)', 'rgba(0,229,255,0.1)']}
          style={styles.referralGradient}
        >
          <View style={styles.referralContent}>
            <Ionicons name="gift" size={24} color="#00e676" />
            <View style={styles.referralText}>
              <Text style={styles.referralTitle}>Refer & Earn</Text>
              <Text style={styles.referralSubtitle}>
                Get 1GB free for every friend who joins
              </Text>
            </View>
          </View>
          <Ionicons name="chevron-forward" size={20} color="#00e676" />
        </LinearGradient>
      </TouchableOpacity>
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
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: '#f0f4f8',
  },
  planCard: {
    marginHorizontal: 20,
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 24,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
    overflow: 'hidden',
  },
  planGradient: {
    flexDirection: 'row',
    padding: 24,
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  planInfo: {
    flex: 1,
  },
  planLabel: {
    color: '#8a9ab0',
    fontSize: 13,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  planName: {
    color: '#f0f4f8',
    fontSize: 22,
    fontWeight: '800',
    marginTop: 4,
  },
  planExpiry: {
    color: '#4a5a70',
    fontSize: 13,
    marginTop: 4,
  },
  dataCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: 'rgba(212,168,83,0.1)',
    borderWidth: 3,
    borderColor: 'rgba(212,168,83,0.3)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  dataPercent: {
    color: '#d4a853',
    fontSize: 24,
    fontWeight: '800',
  },
  dataRemaining: {
    color: '#8a9ab0',
    fontSize: 11,
    fontWeight: '600',
  },
  progressSection: {
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: 'rgba(255,255,255,0.04)',
  },
  progressBackground: {
    height: 8,
    backgroundColor: 'rgba(255,255,255,0.06)',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#00e5ff',
    borderRadius: 4,
  },
  progressFillLow: {
    backgroundColor: '#ff3d3d',
  },
  progressLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  progressLabel: {
    color: '#4a5a70',
    fontSize: 12,
  },
  statsCard: {
    marginHorizontal: 20,
    marginTop: 16,
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  statsTitle: {
    color: '#f0f4f8',
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statItem: {
    alignItems: 'center',
    gap: 8,
  },
  statValue: {
    color: '#f0f4f8',
    fontSize: 16,
    fontWeight: '700',
  },
  statLabel: {
    color: '#4a5a70',
    fontSize: 12,
  },
  plansSection: {
    marginTop: 24,
    paddingHorizontal: 20,
  },
  plansTitle: {
    color: '#f0f4f8',
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 16,
  },
  planOption: {
    borderRadius: 20,
    marginBottom: 12,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  planOptionPopular: {
    borderColor: 'rgba(212,168,83,0.3)',
  },
  planOptionGradient: {
    padding: 20,
  },
  popularBadge: {
    alignSelf: 'flex-start',
    backgroundColor: 'rgba(212,168,83,0.2)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginBottom: 12,
  },
  popularText: {
    color: '#d4a853',
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1,
  },
  planOptionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  planOptionName: {
    color: '#f0f4f8',
    fontSize: 18,
    fontWeight: '700',
  },
  planOptionData: {
    color: '#8a9ab0',
    fontSize: 14,
    marginTop: 2,
  },
  planOptionPrice: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  priceCurrency: {
    color: '#f0f4f8',
    fontSize: 16,
    fontWeight: '600',
  },
  priceAmount: {
    color: '#f0f4f8',
    fontSize: 24,
    fontWeight: '800',
  },
  planFeatures: {
    gap: 8,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  featureText: {
    color: '#8a9ab0',
    fontSize: 13,
  },
  referralBanner: {
    marginHorizontal: 20,
    marginTop: 16,
    marginBottom: 32,
    borderRadius: 16,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(0,230,118,0.2)',
  },
  referralGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    justifyContent: 'space-between',
  },
  referralContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  referralText: {
    gap: 2,
  },
  referralTitle: {
    color: '#00e676',
    fontSize: 16,
    fontWeight: '700',
  },
  referralSubtitle: {
    color: '#8a9ab0',
    fontSize: 13,
  },
});
"""

with open(f'{app_dir}/src/screens/DataScreen.tsx', 'w') as f:
    f.write(data_screen)

# src/screens/AlertsScreen.tsx
alerts_screen = """import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface AlertItem {
  id: string;
  type: 'emergency' | 'network' | 'data' | 'community';
  title: string;
  message: string;
  timestamp: string;
  isRead: boolean;
  priority: 'high' | 'medium' | 'low';
}

const MOCK_ALERTS: AlertItem[] = [
  {
    id: '1',
    type: 'emergency',
    title: 'SOS Signal Received Nearby',
    message: 'A distress signal was detected 500m from your location. Mesh relay active.',
    timestamp: '2 min ago',
    isRead: false,
    priority: 'high',
  },
  {
    id: '2',
    type: 'network',
    title: 'Network Maintenance',
    message: 'DCN tower in Ikeja will undergo maintenance at 2:00 AM. Expect brief interruption.',
    timestamp: '1 hour ago',
    isRead: false,
    priority: 'medium',
  },
  {
    id: '3',
    type: 'data',
    title: 'Data Usage Alert',
    message: 'You have used 80% of your monthly data. Consider upgrading your plan.',
    timestamp: '3 hours ago',
    isRead: true,
    priority: 'medium',
  },
  {
    id: '4',
    type: 'community',
    title: 'New Coverage Area',
    message: 'DCN network is now live in Lekki Phase 1! Enjoy high-speed connectivity.',
    timestamp: '1 day ago',
    isRead: true,
    priority: 'low',
  },
  {
    id: '5',
    type: 'emergency',
    title: 'Weather Warning',
    message: 'Heavy rainfall expected in Lagos. Stay safe and use SOS if needed.',
    timestamp: '2 days ago',
    isRead: true,
    priority: 'high',
  },
];

const getAlertIcon = (type: string) => {
  switch (type) {
    case 'emergency': return 'warning';
    case 'network': return 'cellular';
    case 'data': return 'wifi';
    case 'community': return 'people';
    default: return 'notifications';
  }
};

const getAlertColor = (type: string) => {
  switch (type) {
    case 'emergency': return '#ff3d3d';
    case 'network': return '#00e5ff';
    case 'data': return '#d4a853';
    case 'community': return '#00e676';
    default: return '#8a9ab0';
  }
};

export default function AlertsScreen() {
  const unreadCount = MOCK_ALERTS.filter(a => !a.isRead).length;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>Alerts</Text>
          <Text style={styles.headerSubtitle}>
            {unreadCount} unread notification{unreadCount !== 1 ? 's' : ''}
          </Text>
        </View>
        <TouchableOpacity style={styles.markAllButton}>
          <Text style={styles.markAllText}>Mark all read</Text>
        </TouchableOpacity>
      </View>

      {/* Alerts List */}
      <ScrollView style={styles.list} showsVerticalScrollIndicator={false}>
        {MOCK_ALERTS.map((alert) => (
          <TouchableOpacity
            key={alert.id}
            style={[
              styles.alertCard,
              !alert.isRead && styles.alertCardUnread,
            ]}
            activeOpacity={0.8}
          >
            <View style={[
              styles.alertIcon,
              { backgroundColor: getAlertColor(alert.type) + '15' },
            ]}>
              <Ionicons
                name={getAlertIcon(alert.type) as any}
                size={20}
                color={getAlertColor(alert.type)}
              />
            </View>
            <View style={styles.alertContent}>
              <View style={styles.alertHeader}>
                <Text style={styles.alertTitle}>{alert.title}</Text>
                {alert.priority === 'high' && (
                  <View style={styles.priorityBadge}>
                    <Text style={styles.priorityText}>HIGH</Text>
                  </View>
                )}
              </View>
              <Text style={styles.alertMessage}>{alert.message}</Text>
              <Text style={styles.alertTime}>{alert.timestamp}</Text>
            </View>
            {!alert.isRead && <View style={styles.unreadDot} />}
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050a14',
    paddingTop: 60,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: '#f0f4f8',
  },
  headerSubtitle: {
    color: '#8a9ab0',
    fontSize: 14,
    marginTop: 4,
  },
  markAllButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: 'rgba(212,168,83,0.15)',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: 'rgba(212,168,83,0.25)',
  },
  markAllText: {
    color: '#d4a853',
    fontSize: 12,
    fontWeight: '600',
  },
  list: {
    paddingHorizontal: 20,
  },
  alertCard: {
    flexDirection: 'row',
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 16,
    padding: 16,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.04)',
    gap: 12,
  },
  alertCardUnread: {
    borderColor: 'rgba(212,168,83,0.15)',
    backgroundColor: 'rgba(212,168,83,0.05)',
  },
  alertIcon: {
    width: 44,
    height: 44,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  alertContent: {
    flex: 1,
    gap: 6,
  },
  alertHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  alertTitle: {
    color: '#f0f4f8',
    fontSize: 15,
    fontWeight: '700',
    flex: 1,
  },
  priorityBadge: {
    backgroundColor: 'rgba(255,61,61,0.15)',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  priorityText: {
    color: '#ff3d3d',
    fontSize: 9,
    fontWeight: '800',
  },
  alertMessage: {
    color: '#8a9ab0',
    fontSize: 13,
    lineHeight: 20,
  },
  alertTime: {
    color: '#4a5a70',
    fontSize: 12,
  },
  unreadDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#d4a853',
    marginTop: 4,
  },
});
"""

with open(f'{app_dir}/src/screens/AlertsScreen.tsx', 'w') as f:
    f.write(alerts_screen)

print("DataScreen and AlertsScreen created")
