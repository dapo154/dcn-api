
# src/screens/HomeScreen.tsx
home_screen = """import React, { useEffect } from 'react';
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

import { useAuthStore } from '../store/authStore';
import { useDataStore } from '../store/dataStore';
import { useSOSStore } from '../store/sosStore';

const { width } = Dimensions.get('window');

export default function HomeScreen() {
  const navigation = useNavigation();
  const { user } = useAuthStore();
  const { currentPlan, remainingMB, totalMB, loadDataPlan } = useDataStore();
  const { emergencyContacts, sosHistory } = useSOSStore();

  useEffect(() => {
    loadDataPlan();
  }, []);

  const dataPercentage = totalMB > 0 ? (remainingMB / totalMB) * 100 : 0;
  const recentAlerts = sosHistory.slice(0, 3);

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <LinearGradient
        colors={['rgba(212,168,83,0.15)', 'transparent']}
        style={styles.headerGradient}
      >
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Good Evening,</Text>
            <Text style={styles.name}>{user?.name || 'User'}</Text>
          </View>
          <View style={styles.creditsBadge}>
            <Ionicons name="flash" size={16} color="#d4a853" />
            <Text style={styles.creditsText}>{user?.credits || 0} Credits</Text>
          </View>
        </View>
      </LinearGradient>

      {/* SOS Quick Action */}
      <TouchableOpacity
        style={styles.sosCard}
        onPress={() => navigation.navigate('SOS' as never)}
        activeOpacity={0.8}
      >
        <LinearGradient
          colors={['#ff3d3d', '#ff6b6b']}
          style={styles.sosGradient}
        >
          <Ionicons name="alert-circle" size={32} color="#fff" />
          <View style={styles.sosTextContainer}>
            <Text style={styles.sosTitle}>Emergency SOS</Text>
            <Text style={styles.sosSubtitle}>
              {emergencyContacts.length} contacts configured
            </Text>
          </View>
          <Ionicons name="chevron-forward" size={24} color="#fff" />
        </LinearGradient>
      </TouchableOpacity>

      {/* Data Usage Card */}
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Ionicons name="wifi" size={20} color="#00e5ff" />
          <Text style={styles.cardTitle}>Data Usage</Text>
        </View>
        
        <View style={styles.dataContainer}>
          <View style={styles.dataInfo}>
            <Text style={styles.dataAmount}>
              {remainingMB >= 1024 
                ? `${(remainingMB / 1024).toFixed(1)} GB` 
                : `${remainingMB} MB`}
            </Text>
            <Text style={styles.dataLabel}>
              of {totalMB >= 1024 ? `${(totalMB / 1024).toFixed(1)} GB` : `${totalMB} MB`} remaining
            </Text>
          </View>
          
          <View style={styles.progressContainer}>
            <View style={styles.progressBackground}>
              <View 
                style={[
                  styles.progressFill, 
                  { width: `${dataPercentage}%` },
                  dataPercentage < 20 && styles.progressFillLow
                ]} 
              />
            </View>
            <Text style={styles.progressText}>{Math.round(dataPercentage)}%</Text>
          </View>
        </View>

        <TouchableOpacity 
          style={styles.actionButton}
          onPress={() => navigation.navigate('DataPlans' as never)}
        >
          <Text style={styles.actionButtonText}>Buy More Data</Text>
          <Ionicons name="arrow-forward" size={16} color="#050a14" />
        </TouchableOpacity>
      </View>

      {/* Network Status */}
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Ionicons name="cellular" size={20} color="#00e676" />
          <Text style={styles.cardTitle}>Network Status</Text>
        </View>
        
        <View style={styles.statusGrid}>
          <View style={styles.statusItem}>
            <View style={[styles.statusDot, styles.statusActive]} />
            <Text style={styles.statusLabel}>DCN Network</Text>
            <Text style={styles.statusValue}>Connected</Text>
          </View>
          <View style={styles.statusItem}>
            <View style={[styles.statusDot, styles.statusActive]} />
            <Text style={styles.statusLabel}>Signal</Text>
            <Text style={styles.statusValue}>Excellent</Text>
          </View>
          <View style={styles.statusItem}>
            <View style={[styles.statusDot, styles.statusWarning]} />
            <Text style={styles.statusLabel}>Mesh</Text>
            <Text style={styles.statusValue}>2 Peers</Text>
          </View>
        </View>
      </View>

      {/* Recent Alerts */}
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Ionicons name="notifications" size={20} color="#d4a853" />
          <Text style={styles.cardTitle}>Recent Alerts</Text>
        </View>
        
        {recentAlerts.length === 0 ? (
          <Text style={styles.emptyText}>No recent alerts</Text>
        ) : (
          recentAlerts.map((alert) => (
            <View key={alert.id} style={styles.alertItem}>
              <View style={styles.alertIcon}>
                <Ionicons name="warning" size={16} color="#ff3d3d" />
              </View>
              <View style={styles.alertContent}>
                <Text style={styles.alertTitle}>SOS Triggered</Text>
                <Text style={styles.alertTime}>
                  {new Date(alert.timestamp).toLocaleString()}
                </Text>
              </View>
              <View style={[
                styles.alertStatus,
                alert.status === 'resolved' && styles.alertStatusResolved
              ]}>
                <Text style={styles.alertStatusText}>
                  {alert.status.toUpperCase()}
                </Text>
              </View>
            </View>
          ))
        )}
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActions}>
        <TouchableOpacity 
          style={styles.quickAction}
          onPress={() => navigation.navigate('EmergencyContacts' as never)}
        >
          <View style={[styles.quickIcon, { backgroundColor: 'rgba(212,168,83,0.15)' }]}>
            <Ionicons name="people" size={24} color="#d4a853" />
          </View>
          <Text style={styles.quickLabel}>Contacts</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.quickAction}>
          <View style={[styles.quickIcon, { backgroundColor: 'rgba(0,229,255,0.15)' }]}>
            <Ionicons name="map" size={24} color="#00e5ff" />
          </View>
          <Text style={styles.quickLabel}>Coverage</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.quickAction}>
          <View style={[styles.quickIcon, { backgroundColor: 'rgba(0,230,118,0.15)' }]}>
            <Ionicons name="gift" size={24} color="#00e676" />
          </View>
          <Text style={styles.quickLabel}>Referral</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.quickAction}>
          <View style={[styles.quickIcon, { backgroundColor: 'rgba(255,61,61,0.15)' }]}>
            <Ionicons name="call" size={24} color="#ff3d3d" />
          </View>
          <Text style={styles.quickLabel}>Support</Text>
        </TouchableOpacity>
      </View>

      <View style={{ height: 32 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050a14',
  },
  headerGradient: {
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  greeting: {
    fontSize: 14,
    color: '#8a9ab0',
    fontWeight: '500',
  },
  name: {
    fontSize: 24,
    fontWeight: '800',
    color: '#f0f4f8',
    marginTop: 4,
  },
  creditsBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(212,168,83,0.15)',
    borderWidth: 1,
    borderColor: 'rgba(212,168,83,0.25)',
    borderRadius: 20,
    paddingHorizontal: 12,
    paddingVertical: 6,
    gap: 6,
  },
  creditsText: {
    color: '#d4a853',
    fontWeight: '700',
    fontSize: 13,
  },
  sosCard: {
    marginHorizontal: 20,
    marginTop: 8,
    borderRadius: 16,
    overflow: 'hidden',
  },
  sosGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    gap: 16,
  },
  sosTextContainer: {
    flex: 1,
  },
  sosTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '800',
  },
  sosSubtitle: {
    color: 'rgba(255,255,255,0.8)',
    fontSize: 13,
    marginTop: 2,
  },
  card: {
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 20,
    padding: 20,
    marginHorizontal: 20,
    marginTop: 16,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 16,
  },
  cardTitle: {
    color: '#f0f4f8',
    fontSize: 16,
    fontWeight: '700',
  },
  dataContainer: {
    gap: 12,
  },
  dataInfo: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: 8,
  },
  dataAmount: {
    color: '#f0f4f8',
    fontSize: 32,
    fontWeight: '800',
  },
  dataLabel: {
    color: '#8a9ab0',
    fontSize: 14,
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  progressBackground: {
    flex: 1,
    height: 8,
    backgroundColor: 'rgba(255,255,255,0.08)',
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
  progressText: {
    color: '#8a9ab0',
    fontSize: 13,
    fontWeight: '600',
    width: 36,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#d4a853',
    borderRadius: 12,
    paddingVertical: 12,
    marginTop: 16,
    gap: 8,
  },
  actionButtonText: {
    color: '#050a14',
    fontWeight: '700',
    fontSize: 14,
  },
  statusGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statusItem: {
    alignItems: 'center',
    gap: 6,
  },
  statusDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
  },
  statusActive: {
    backgroundColor: '#00e676',
  },
  statusWarning: {
    backgroundColor: '#f0c96a',
  },
  statusLabel: {
    color: '#8a9ab0',
    fontSize: 12,
  },
  statusValue: {
    color: '#f0f4f8',
    fontSize: 13,
    fontWeight: '600',
  },
  alertItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.04)',
    gap: 12,
  },
  alertIcon: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: 'rgba(255,61,61,0.1)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  alertContent: {
    flex: 1,
  },
  alertTitle: {
    color: '#f0f4f8',
    fontWeight: '600',
    fontSize: 14,
  },
  alertTime: {
    color: '#8a9ab0',
    fontSize: 12,
    marginTop: 2,
  },
  alertStatus: {
    backgroundColor: 'rgba(255,61,61,0.15)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  alertStatusResolved: {
    backgroundColor: 'rgba(0,230,118,0.15)',
  },
  alertStatusText: {
    color: '#ff3d3d',
    fontSize: 10,
    fontWeight: '700',
  },
  emptyText: {
    color: '#4a5a70',
    textAlign: 'center',
    paddingVertical: 16,
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginHorizontal: 20,
    marginTop: 20,
  },
  quickAction: {
    alignItems: 'center',
    gap: 8,
  },
  quickIcon: {
    width: 56,
    height: 56,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  quickLabel: {
    color: '#8a9ab0',
    fontSize: 12,
    fontWeight: '500',
  },
});
"""

with open(f'{app_dir}/src/screens/HomeScreen.tsx', 'w') as f:
    f.write(home_screen)

print("HomeScreen created")
