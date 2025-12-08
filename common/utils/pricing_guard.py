"""
Pricing Guard Middleware
Enforces free-tier and subscription-based access control for Nexora Suite.

FREE TIER: Until March 31, 2026 - All features available
PRICING ACTIVE: From April 1, 2026 - Premium features require active subscription
"""

from datetime import datetime, timezone
from functools import wraps
from flask import request, jsonify, session
from typing import Callable, Any, Optional

# Free tier cutoff date: March 31, 2026, 23:59:59 UTC
FREE_UNTIL = datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc)

# Feature tiers - Define which features require premium subscription
PREMIUM_FEATURES = {
    "advanced_reports": {"tier": "professional", "description": "Advanced analytics and reporting"},
    "api_access": {"tier": "professional", "description": "API access for integrations"},
    "custom_branding": {"tier": "enterprise", "description": "Custom branding and white-label"},
    "webhook_integrations": {"tier": "professional", "description": "Webhook integrations"},
    "bulk_operations": {"tier": "professional", "description": "Bulk import/export operations"},
    "advanced_payroll": {"tier": "professional", "description": "Advanced payroll features"},
    "multi_branch": {"tier": "professional", "description": "Multiple branch management"},
    "team_collaboration": {"tier": "professional", "description": "Team collaboration tools"},
}

SUBSCRIPTION_TIERS = {
    "free": {"price": 0, "features": []},
    "professional": {"price": 99, "features": list(PREMIUM_FEATURES.keys())},
    "enterprise": {"price": 499, "features": list(PREMIUM_FEATURES.keys())},
}


def is_free_tier_active() -> bool:
    """
    Check if we're still in the free tier period.
    
    Returns:
        bool: True if current time is before April 1, 2026, False otherwise
    """
    now = datetime.now(timezone.utc)
    return now <= FREE_UNTIL


def get_pricing_status() -> dict:
    """
    Get current pricing status information.
    
    Returns:
        dict: Status information including free_tier_active, days_remaining, etc.
    """
    now = datetime.now(timezone.utc)
    free_active = is_free_tier_active()
    days_remaining = (FREE_UNTIL - now).days if free_active else 0
    
    return {
        "free_tier_active": free_active,
        "free_until": FREE_UNTIL.isoformat(),
        "pricing_active_from": "2026-04-01T00:00:00Z",
        "days_remaining": max(0, days_remaining),
        "current_date": now.isoformat(),
    }


def check_subscription_status(subscription_status: Optional[str] = None) -> bool:
    """
    Check if subscription is active (for post-March-31-2026).
    
    Args:
        subscription_status: The subscription tier (free, professional, enterprise)
        
    Returns:
        bool: True if subscription is active or in free tier, False otherwise
    """
    if is_free_tier_active():
        return True
    
    # After March 31, 2026, require active subscription
    return subscription_status in ["professional", "enterprise"]


def get_user_subscription_status(user_data: dict) -> dict:
    """
    Get subscription status from user data.
    
    Args:
        user_data: User session or auth data
        
    Returns:
        dict: Subscription status information
    """
    subscription_tier = user_data.get("subscription_tier", "free")
    is_active = user_data.get("subscription_active", False)
    
    return {
        "tier": subscription_tier,
        "is_active": is_active,
        "can_access": check_subscription_status(subscription_tier if is_active else None),
    }


def pricing_guard(feature: Optional[str] = None) -> Callable:
    """
    Decorator to protect routes with pricing guards.
    
    Usage:
        @app.route('/api/advanced-reports')
        @pricing_guard(feature='advanced_reports')
        def advanced_reports():
            return {"data": "..."}
        
        # Or without feature check (allows all if free tier, requires subscription after)
        @app.route('/api/protected')
        @pricing_guard()
        def protected_route():
            return {"data": "..."}
    
    Args:
        feature: Optional feature name to check for premium requirement
        
    Returns:
        Callable: Decorator function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs) -> Any:
            # If still in free tier, allow everything
            if is_free_tier_active():
                return f(*args, **kwargs)
            
            # After March 31, 2026 - check subscription
            user_data = session.get("user", {})
            subscription_tier = user_data.get("subscription_tier", "free")
            is_subscription_active = user_data.get("subscription_active", False)
            
            # Check if user has active subscription
            if not is_subscription_active:
                return jsonify({
                    "error": "Premium feature requires active subscription",
                    "feature": feature or "premium_access",
                    "pricing_info": get_pricing_status(),
                    "subscription_tiers": SUBSCRIPTION_TIERS,
                }), 402  # 402 Payment Required
            
            # Check specific feature if provided
            if feature and feature in PREMIUM_FEATURES:
                required_tier = PREMIUM_FEATURES[feature]["tier"]
                if subscription_tier not in SUBSCRIPTION_TIERS:
                    subscription_tier = "free"
                
                # Check if user's tier covers this feature
                if subscription_tier == "free":
                    return jsonify({
                        "error": f"Feature '{feature}' requires {required_tier} subscription",
                        "feature": feature,
                        "required_tier": required_tier,
                        "pricing_info": get_pricing_status(),
                        "subscription_tiers": SUBSCRIPTION_TIERS,
                    }), 402  # 402 Payment Required
                
                # Enterprise can access everything, professional can access professional+
                if required_tier == "enterprise" and subscription_tier == "professional":
                    return jsonify({
                        "error": f"Feature '{feature}' requires {required_tier} subscription",
                        "feature": feature,
                        "required_tier": required_tier,
                        "current_tier": subscription_tier,
                        "pricing_info": get_pricing_status(),
                    }), 402
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def pricing_required(f: Callable) -> Callable:
    """
    Simple decorator to require either free tier or active subscription.
    
    Usage:
        @app.route('/api/protected')
        @pricing_required
        def protected_route():
            return {"data": "..."}
    """
    return pricing_guard(feature=None)(f)


def apply_pricing_middleware(app) -> None:
    """
    Apply pricing information to all responses.
    
    This adds pricing headers to every response for client-side awareness.
    
    Args:
        app: Flask application instance
    """
    @app.after_request
    def add_pricing_headers(response):
        """Add pricing status headers to all responses."""
        pricing_status = get_pricing_status()
        
        response.headers["X-Pricing-Free-Tier-Active"] = str(pricing_status["free_tier_active"]).lower()
        response.headers["X-Pricing-Free-Until"] = pricing_status["free_until"]
        response.headers["X-Pricing-Active-From"] = pricing_status["pricing_active_from"]
        
        if pricing_status["days_remaining"] > 0:
            response.headers["X-Pricing-Days-Remaining"] = str(pricing_status["days_remaining"])
        
        return response


def get_banner_data() -> dict:
    """
    Get banner data for frontend display.
    
    Returns:
        dict: Banner information including message, styling, and action
    """
    pricing_status = get_pricing_status()
    
    if pricing_status["free_tier_active"]:
        return {
            "visible": True,
            "type": "success",
            "message": f"🎉 Free until March 31, 2026. Pricing activates from April 1, 2026.",
            "subtext": f"{pricing_status['days_remaining']} days remaining in free tier.",
            "action": "Learn more about our pricing plans",
            "action_url": "/pricing",
            "dismissible": False,
        }
    else:
        return {
            "visible": True,
            "type": "info",
            "message": "Pricing is now active. Some features require an active subscription.",
            "subtext": "Upgrade to Professional or Enterprise for unlimited access.",
            "action": "View subscription plans",
            "action_url": "/subscription",
            "dismissible": True,
        }


# Export public API
__all__ = [
    "FREE_UNTIL",
    "PREMIUM_FEATURES",
    "SUBSCRIPTION_TIERS",
    "is_free_tier_active",
    "get_pricing_status",
    "check_subscription_status",
    "get_user_subscription_status",
    "pricing_guard",
    "pricing_required",
    "apply_pricing_middleware",
    "get_banner_data",
]
