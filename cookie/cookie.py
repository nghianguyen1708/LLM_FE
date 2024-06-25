import streamlit as st
import streamlit.components.v1 as components


class CookieController:
    def __init__(self, key):
        self.key = key

    def set(self, name, value, max_age=60 * 60 * 24 * 30):
        set_cookie_js = f"""
        <script>
        function setCookie(name, value, days) {{
            var expires = "";
            if (days) {{
                var date = new Date();
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                expires = "; expires=" + date.toUTCString();
            }}
            document.cookie = name + "=" + (value || "")  + expires + "; path=/";
            location.reload();
        }}
        setCookie('{name}', '{value}', {max_age / (24 * 60 * 60)});
        </script>
        """
        components.html(set_cookie_js)

    def get(self, name):
        get_cookie_js = f"""
        <script>
        function getCookie(name) {{
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {{
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }}
            return null;
        }}
        const cookieValue = getCookie('{name}');
        const streamlitCallback = window.streamlitApi.setComponentValue;
        if (streamlitCallback) {{
            streamlitCallback(cookieValue);
        }}
        location.reload();
        </script>
        """
        cookie_value = components.html(get_cookie_js, height=0, width=0)
        from streamlit_cookies_controller import CookieController
        controller = CookieController("cookies")
        return controller.get("access_token")

    # Function to erase the cookie using JavaScript
    def erase_cookie_js(self, name):
        js_code = f"""
        <script>
            function eraseCookie(name) {{
                document.cookie = name + '=; Max-Age=-99999999;';
            }}
            eraseCookie('{name}');
            location.reload();
        </script>
        """
        components.html(js_code)


cookie_controller = CookieController(key='cookies')
