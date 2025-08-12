#!/usr/bin/env python3
"""
強化版Netlify監視システム
ビルドログの詳細取得による精密エラー解析

Author: Claude Code
Date: 2025-08-10
"""

import requests
import json
import time
import logging

class EnhancedNetlifyMonitor:
    """詳細ビルドログ解析機能付きNetlify監視"""
    
    def __init__(self):
        self.site_id = "178502f5-7910-4db3-bfd1-ae57d99e9345"
        self.base_url = "https://api.netlify.com/api/v1"
        
    def get_deploy_details(self, deploy_id):
        """デプロイの詳細情報とビルドログを取得"""
        
        try:
            # デプロイ詳細取得
            deploy_url = f"{self.base_url}/deploys/{deploy_id}"
            deploy_response = requests.get(deploy_url, timeout=10)
            
            if deploy_response.status_code != 200:
                print(f"❌ デプロイ詳細取得失敗: {deploy_response.status_code}")
                return None
                
            deploy_data = deploy_response.json()
            
            # ビルドログ取得 (可能な場合)
            build_log_url = f"{self.base_url}/sites/{self.site_id}/deploys/{deploy_id}/log"
            log_response = requests.get(build_log_url, timeout=15)
            
            build_log = ""
            if log_response.status_code == 200:
                build_log = log_response.text
            else:
                print(f"⚠️ ビルドログ取得失敗 (認証が必要な可能性): {log_response.status_code}")
                build_log = "ログ取得不可"
            
            return {
                'deploy_data': deploy_data,
                'build_log': build_log,
                'error_message': deploy_data.get('error_message', ''),
                'state': deploy_data.get('state', ''),
                'deploy_time': deploy_data.get('deploy_time', 0)
            }
            
        except Exception as e:
            print(f"❌ デプロイ詳細取得エラー: {e}")
            return None
    
    def analyze_ruby_errors_from_log(self, build_log):
        """ビルドログからRuby gemエラーを詳細解析"""
        
        if not build_log or build_log == "ログ取得不可":
            return []
            
        ruby_gem_patterns = [
            'cannot load such file -- ',
            'LoadError',
            'Bundler::GemNotFound',
            'Could not find gem',
            'bundler: failed to load command:'
        ]
        
        found_errors = []
        lines = build_log.split('\n')
        
        for line in lines:
            for pattern in ruby_gem_patterns:
                if pattern in line:
                    # gem名を抽出
                    if 'cannot load such file --' in line:
                        gem_name = line.split('cannot load such file --')[1].strip().split()[0].strip('\'\"()')
                        found_errors.append(f"Missing gem: {gem_name}")
                    elif 'Could not find' in line and 'gem' in line:
                        found_errors.append(f"Gem not found: {line}")
                    else:
                        found_errors.append(f"Ruby error: {line}")
                        
        return found_errors
    
    def test_latest_failed_deploy(self):
        """最新の失敗デプロイを解析"""
        
        print("🔍 最新の失敗デプロイ解析中...")
        
        # 最新デプロイ一覧取得
        try:
            deploys_url = f"{self.base_url}/sites/{self.site_id}/deploys"
            response = requests.get(deploys_url, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ デプロイ一覧取得失敗: {response.status_code}")
                return
                
            deploys = response.json()
            
            # 最新のエラーデプロイを検索
            failed_deploy = None
            for deploy in deploys[:5]:  # 最新5件をチェック
                if deploy.get('state') == 'error':
                    failed_deploy = deploy
                    break
            
            if not failed_deploy:
                print("✅ 最近の失敗デプロイが見つかりません")
                return
                
            print(f"📊 失敗デプロイ発見: {failed_deploy['id']}")
            print(f"   作成日時: {failed_deploy.get('created_at', 'N/A')}")
            
            # 詳細解析
            details = self.get_deploy_details(failed_deploy['id'])
            
            if details:
                print(f"\n📋 デプロイ詳細:")
                print(f"   状態: {details['state']}")
                print(f"   エラーメッセージ: {details['error_message']}")
                print(f"   ビルド時間: {details['deploy_time']}秒")
                
                # ビルドログからRubyエラー解析
                ruby_errors = self.analyze_ruby_errors_from_log(details['build_log'])
                
                if ruby_errors:
                    print(f"\n🔥 検出されたRubyエラー ({len(ruby_errors)}件):")
                    for i, error in enumerate(ruby_errors[:5], 1):
                        print(f"   {i}. {error}")
                else:
                    print("\n💡 具体的なRuby gemエラーは検出されませんでした")
                    
                # ログのサンプル表示
                if details['build_log'] != "ログ取得不可":
                    log_lines = details['build_log'].split('\n')
                    print(f"\n📄 ビルドログ抜粋 (最後の20行):")
                    for line in log_lines[-20:]:
                        if line.strip():
                            print(f"   {line}")
                            
        except Exception as e:
            print(f"❌ 解析エラー: {e}")

def main():
    monitor = EnhancedNetlifyMonitor()
    monitor.test_latest_failed_deploy()

if __name__ == '__main__':
    main()