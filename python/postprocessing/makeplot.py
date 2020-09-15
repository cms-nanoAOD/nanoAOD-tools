




<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  <link rel="dns-prefetch" href="https://github.githubassets.com">
  <link rel="dns-prefetch" href="https://avatars0.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars1.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars2.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars3.githubusercontent.com">
  <link rel="dns-prefetch" href="https://github-cloud.s3.amazonaws.com">
  <link rel="dns-prefetch" href="https://user-images.githubusercontent.com/">



  <link crossorigin="anonymous" media="all" integrity="sha512-lC+Z9kBc6E9r9umj6DgEEoQP7CX8RgGJGegRUJbthY1Bus2eemD1Kkc1Wbacj7hxeuvVCuyeqfNsKZWxqt1uIw==" rel="stylesheet" href="https://github.githubassets.com/assets/frameworks-942f99f6405ce84f6bf6e9a3e8380412.css" />
  <link crossorigin="anonymous" media="all" integrity="sha512-Z0DkfbFb4XDoclqPgW0w4WQrnjY2nXN7PcppfsWW1hb5bo+svzJcNTJ/eYyUHHlbgefLjcVE4g0aW4qrmHXjSg==" rel="stylesheet" href="https://github.githubassets.com/assets/site-6740e47db15be170e8725a8f816d30e1.css" />
    <link crossorigin="anonymous" media="all" integrity="sha512-h6JvvHSZfEUhchI8zIqcW1sUEpr2MWrdrWmjJ9im+uMcTItXLbmsd2XLTHnlD79dTU93P0S00lIbuXWdgnrrTQ==" rel="stylesheet" href="https://github.githubassets.com/assets/github-87a26fbc74997c452172123ccc8a9c5b.css" />
    
    
    
    


  <meta name="viewport" content="width=device-width">
  
  <title>nanoAOD-tools/makeplot.py at master · adeiorio/nanoAOD-tools · GitHub</title>
    <meta name="description" content="Tools for working with NanoAOD (requiring only python + root, not CMSSW) - adeiorio/nanoAOD-tools">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
  <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
  <meta property="fb:app_id" content="1401488693436528">
  <meta name="apple-itunes-app" content="app-id=1477376905">

    <meta name="twitter:image:src" content="https://avatars2.githubusercontent.com/u/28299733?s=400&amp;v=4" /><meta name="twitter:site" content="@github" /><meta name="twitter:card" content="summary" /><meta name="twitter:title" content="adeiorio/nanoAOD-tools" /><meta name="twitter:description" content="Tools for working with NanoAOD (requiring only python + root, not CMSSW) - adeiorio/nanoAOD-tools" />
    <meta property="og:image" content="https://avatars2.githubusercontent.com/u/28299733?s=400&amp;v=4" /><meta property="og:site_name" content="GitHub" /><meta property="og:type" content="object" /><meta property="og:title" content="adeiorio/nanoAOD-tools" /><meta property="og:url" content="https://github.com/adeiorio/nanoAOD-tools" /><meta property="og:description" content="Tools for working with NanoAOD (requiring only python + root, not CMSSW) - adeiorio/nanoAOD-tools" />



  

  <link rel="assets" href="https://github.githubassets.com/">
  

  <meta name="request-id" content="B272:7D26:9A8180:DF788E:5F6075FA" data-pjax-transient="true"/><meta name="html-safe-nonce" content="ca97ebc38c4c9ffe683faf0dc366d2e9e69dfef1" data-pjax-transient="true"/><meta name="visitor-payload" content="eyJyZWZlcnJlciI6IiIsInJlcXVlc3RfaWQiOiJCMjcyOjdEMjY6OUE4MTgwOkRGNzg4RTo1RjYwNzVGQSIsInZpc2l0b3JfaWQiOiI5MDcxMDY1ODA2NTc5NzI1ODE4IiwicmVnaW9uX2VkZ2UiOiJmcmEiLCJyZWdpb25fcmVuZGVyIjoiZnJhIn0=" data-pjax-transient="true"/><meta name="visitor-hmac" content="5a36f9908984990fa049686d87efd73ad2545bae3547529c5f6c269e11cfb5aa" data-pjax-transient="true"/><meta name="cookie-consent-required" content="false" data-pjax-transient="true"/>

    <meta name="hovercard-subject-tag" content="repository:222721731" data-pjax-transient>


  <meta name="github-keyboard-shortcuts" content="repository,source-code" data-pjax-transient="true" />

  

  <meta name="selected-link" value="repo_source" data-pjax-transient>

    <meta name="google-site-verification" content="c1kuD-K2HIVF635lypcsWPoD4kilo5-jA_wBFyT4uMY">
  <meta name="google-site-verification" content="KT5gs8h0wvaagLKAVWq8bbeNwnZZK1r1XQysX3xurLU">
  <meta name="google-site-verification" content="ZzhVyEFwb7w3e0-uOTltm8Jsck2F5StVihD0exw2fsA">
  <meta name="google-site-verification" content="GXs5KoUUkNCoaAZn7wPN-t01Pywp9M3sEjnt_3_ZWPc">

  <meta name="octolytics-host" content="collector.githubapp.com" /><meta name="octolytics-app-id" content="github" /><meta name="octolytics-event-url" content="https://collector.githubapp.com/github-external/browser_event" /><meta name="octolytics-dimension-ga_id" content="" class="js-octo-ga-id" />

  <meta name="analytics-location" content="/&lt;user-name&gt;/&lt;repo-name&gt;/blob/show" data-pjax-transient="true" />

  





    <meta name="google-analytics" content="UA-3769691-2">


<meta class="js-ga-set" name="dimension10" content="Responsive" data-pjax-transient>

<meta class="js-ga-set" name="dimension1" content="Logged Out">



  

      <meta name="hostname" content="github.com">
    <meta name="user-login" content="">


      <meta name="expected-hostname" content="github.com">


    <meta name="enabled-features" content="MARKETPLACE_PENDING_INSTALLATIONS">

  <meta http-equiv="x-pjax-version" content="f7b5d317736de7d190e6449d66af9e9f">
  

        <link href="https://github.com/adeiorio/nanoAOD-tools/commits/master.atom" rel="alternate" title="Recent Commits to nanoAOD-tools:master" type="application/atom+xml">

  <meta name="go-import" content="github.com/adeiorio/nanoAOD-tools git https://github.com/adeiorio/nanoAOD-tools.git">

  <meta name="octolytics-dimension-user_id" content="28299733" /><meta name="octolytics-dimension-user_login" content="adeiorio" /><meta name="octolytics-dimension-repository_id" content="222721731" /><meta name="octolytics-dimension-repository_nwo" content="adeiorio/nanoAOD-tools" /><meta name="octolytics-dimension-repository_public" content="true" /><meta name="octolytics-dimension-repository_is_fork" content="true" /><meta name="octolytics-dimension-repository_parent_id" content="104048162" /><meta name="octolytics-dimension-repository_parent_nwo" content="cms-nanoAOD/nanoAOD-tools" /><meta name="octolytics-dimension-repository_network_root_id" content="104048162" /><meta name="octolytics-dimension-repository_network_root_nwo" content="cms-nanoAOD/nanoAOD-tools" /><meta name="octolytics-dimension-repository_explore_github_marketplace_ci_cta_shown" content="false" />


    <link rel="canonical" href="https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py" data-pjax-transient>


  <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">

  <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">

  <link rel="mask-icon" href="https://github.githubassets.com/pinned-octocat.svg" color="#000000">
  <link rel="alternate icon" class="js-site-favicon" type="image/png" href="https://github.githubassets.com/favicons/favicon.png">
  <link rel="icon" class="js-site-favicon" type="image/svg+xml" href="https://github.githubassets.com/favicons/favicon.svg">

<meta name="theme-color" content="#1e2327">


  <link rel="manifest" href="/manifest.json" crossOrigin="use-credentials">

  </head>

  <body class="logged-out env-production page-responsive page-blob">
    

    <div class="position-relative js-header-wrapper ">
      <a href="#start-of-content" class="px-2 py-4 bg-blue text-white show-on-focus js-skip-to-content">Skip to content</a>
      <span class="progress-pjax-loader width-full js-pjax-loader-bar Progress position-fixed">
    <span style="background-color: #79b8ff;width: 0%;" class="Progress-item progress-pjax-loader-bar "></span>
</span>      
      



          <header class="Header-old header-logged-out js-details-container Details position-relative f4 py-2" role="banner">
  <div class="container-xl d-lg-flex flex-items-center p-responsive">
    <div class="d-flex flex-justify-between flex-items-center">
        <a class="mr-4" href="https://github.com/" aria-label="Homepage" data-ga-click="(Logged out) Header, go to homepage, icon:logo-wordmark">
          <svg height="32" class="octicon octicon-mark-github text-white" viewBox="0 0 16 16" version="1.1" width="32" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
        </a>

          <div class="d-lg-none css-truncate css-truncate-target width-fit p-2">
            

          </div>

        <div class="d-flex flex-items-center">
              <a href="/join?ref_cta=Sign+up&amp;ref_loc=header+logged+out&amp;ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E%2Fblob%2Fshow&amp;source=header-repo"
                class="d-inline-block d-lg-none f5 text-white no-underline border border-gray-dark rounded-2 px-2 py-1 mr-3 mr-sm-5"
                data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;site header&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;SIGN_UP&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="ad371265a6fdf2de416c172f595f20696a17fd020c97cc9f7571926b396d36d2"
                data-ga-click="Sign up, click to sign up for account, ref_page:/&lt;user-name&gt;/&lt;repo-name&gt;/blob/show;ref_cta:Sign up;ref_loc:header logged out">
                Sign&nbsp;up
              </a>

          <button class="btn-link d-lg-none mt-1 js-details-target" type="button" aria-label="Toggle navigation" aria-expanded="false">
            <svg height="24" class="octicon octicon-three-bars text-white" viewBox="0 0 16 16" version="1.1" width="24" aria-hidden="true"><path fill-rule="evenodd" d="M1 2.75A.75.75 0 011.75 2h12.5a.75.75 0 110 1.5H1.75A.75.75 0 011 2.75zm0 5A.75.75 0 011.75 7h12.5a.75.75 0 110 1.5H1.75A.75.75 0 011 7.75zM1.75 12a.75.75 0 100 1.5h12.5a.75.75 0 100-1.5H1.75z"></path></svg>
          </button>
        </div>
    </div>

    <div class="HeaderMenu HeaderMenu--logged-out position-fixed top-0 right-0 bottom-0 height-fit position-lg-relative d-lg-flex flex-justify-between flex-items-center flex-auto">
      <div class="d-flex d-lg-none flex-justify-end border-bottom bg-gray-light p-3">
        <button class="btn-link js-details-target" type="button" aria-label="Toggle navigation" aria-expanded="false">
          <svg height="24" class="octicon octicon-x text-gray" viewBox="0 0 24 24" version="1.1" width="24" aria-hidden="true"><path fill-rule="evenodd" d="M5.72 5.72a.75.75 0 011.06 0L12 10.94l5.22-5.22a.75.75 0 111.06 1.06L13.06 12l5.22 5.22a.75.75 0 11-1.06 1.06L12 13.06l-5.22 5.22a.75.75 0 01-1.06-1.06L10.94 12 5.72 6.78a.75.75 0 010-1.06z"></path></svg>
        </button>
      </div>

        <nav class="mt-0 px-3 px-lg-0 mb-5 mb-lg-0" aria-label="Global">
          <ul class="d-lg-flex list-style-none">
              <li class="d-block d-lg-flex flex-lg-nowrap flex-lg-items-center border-bottom border-lg-bottom-0 mr-0 mr-lg-3 edge-item-fix position-relative flex-wrap flex-justify-between d-flex flex-items-center ">
                <details class="HeaderMenu-details details-overlay details-reset width-full">
                  <summary class="HeaderMenu-summary HeaderMenu-link px-0 py-3 border-0 no-wrap d-block d-lg-inline-block">
                    Why GitHub?
                    <svg x="0px" y="0px" viewBox="0 0 14 8" xml:space="preserve" fill="none" class="icon-chevon-down-mktg position-absolute position-lg-relative">
                      <path d="M1,1l6.2,6L13,1"></path>
                    </svg>
                  </summary>
                  <div class="dropdown-menu flex-auto rounded-1 bg-white px-0 mt-0 pb-4 p-lg-4 position-relative position-lg-absolute left-0 left-lg-n4">
                    <a href="/features" class="py-2 lh-condensed-ultra d-block link-gray-dark no-underline h5 Bump-link--hover" data-ga-click="(Logged out) Header, go to Features">Features <span class="Bump-link-symbol float-right text-normal text-gray-light">&rarr;</span></a>
                    <ul class="list-style-none f5 pb-3">
                      <li class="edge-item-fix"><a href="/features/code-review/" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Code review">Code review</a></li>
                      <li class="edge-item-fix"><a href="/features/project-management/" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Project management">Project management</a></li>
                      <li class="edge-item-fix"><a href="/features/integrations" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Integrations">Integrations</a></li>
                      <li class="edge-item-fix"><a href="/features/actions" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Actions">Actions</a></li>
                      <li class="edge-item-fix"><a href="/features/packages" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to GitHub Packages">Packages</a></li>
                      <li class="edge-item-fix"><a href="/features/security" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Security">Security</a></li>
                      <li class="edge-item-fix"><a href="/features#team-management" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Team management">Team management</a></li>
                      <li class="edge-item-fix"><a href="/features#hosting" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Code hosting">Hosting</a></li>
                      <li class="edge-item-fix hide-xl"><a href="/mobile" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Mobile">Mobile</a></li>
                    </ul>

                    <ul class="list-style-none mb-0 border-lg-top pt-lg-3">
                      <li class="edge-item-fix"><a href="/customer-stories" class="py-2 lh-condensed-ultra d-block no-underline link-gray-dark no-underline h5 Bump-link--hover" data-ga-click="(Logged out) Header, go to Customer stories">Customer stories <span class="Bump-link-symbol float-right text-normal text-gray-light">&rarr;</span></a></li>
                      <li class="edge-item-fix"><a href="/security" class="py-2 lh-condensed-ultra d-block no-underline link-gray-dark no-underline h5 Bump-link--hover" data-ga-click="(Logged out) Header, go to Security">Security <span class="Bump-link-symbol float-right text-normal text-gray-light">&rarr;</span></a></li>
                    </ul>
                  </div>
                </details>
              </li>
              <li class="border-bottom border-lg-bottom-0 mr-0 mr-lg-3">
                <a href="/team" class="HeaderMenu-link no-underline py-3 d-block d-lg-inline-block" data-ga-click="(Logged out) Header, go to Team">Team</a>
              </li>
              <li class="border-bottom border-lg-bottom-0 mr-0 mr-lg-3">
                <a href="/enterprise" class="HeaderMenu-link no-underline py-3 d-block d-lg-inline-block" data-ga-click="(Logged out) Header, go to Enterprise">Enterprise</a>
              </li>

              <li class="d-block d-lg-flex flex-lg-nowrap flex-lg-items-center border-bottom border-lg-bottom-0 mr-0 mr-lg-3 edge-item-fix position-relative flex-wrap flex-justify-between d-flex flex-items-center ">
                <details class="HeaderMenu-details details-overlay details-reset width-full">
                  <summary class="HeaderMenu-summary HeaderMenu-link px-0 py-3 border-0 no-wrap d-block d-lg-inline-block">
                    Explore
                    <svg x="0px" y="0px" viewBox="0 0 14 8" xml:space="preserve" fill="none" class="icon-chevon-down-mktg position-absolute position-lg-relative">
                      <path d="M1,1l6.2,6L13,1"></path>
                    </svg>
                  </summary>

                  <div class="dropdown-menu flex-auto rounded-1 bg-white px-0 pt-2 pb-0 mt-0 pb-4 p-lg-4 position-relative position-lg-absolute left-0 left-lg-n4">
                    <ul class="list-style-none mb-3">
                      <li class="edge-item-fix"><a href="/explore" class="py-2 lh-condensed-ultra d-block link-gray-dark no-underline h5 Bump-link--hover" data-ga-click="(Logged out) Header, go to Explore">Explore GitHub <span class="Bump-link-symbol float-right text-normal text-gray-light">&rarr;</span></a></li>
                    </ul>

                    <h4 class="text-gray-light text-normal text-mono f5 mb-2 border-lg-top pt-lg-3">Learn &amp; contribute</h4>
                    <ul class="list-style-none mb-3">
                      <li class="edge-item-fix"><a href="/topics" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Topics">Topics</a></li>
                        <li class="edge-item-fix"><a href="/collections" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Collections">Collections</a></li>
                      <li class="edge-item-fix"><a href="/trending" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Trending">Trending</a></li>
                      <li class="edge-item-fix"><a href="https://lab.github.com/" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Learning lab">Learning Lab</a></li>
                      <li class="edge-item-fix"><a href="https://opensource.guide" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Open source guides">Open source guides</a></li>
                    </ul>

                    <h4 class="text-gray-light text-normal text-mono f5 mb-2 border-lg-top pt-lg-3">Connect with others</h4>
                    <ul class="list-style-none mb-0">
                      <li class="edge-item-fix"><a href="https://github.com/events" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Events">Events</a></li>
                      <li class="edge-item-fix"><a href="https://github.community" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Community forum">Community forum</a></li>
                      <li class="edge-item-fix"><a href="https://education.github.com" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to GitHub Education">GitHub Education</a></li>
                      <li class="edge-item-fix"><a href="https://stars.github.com" class="py-2 pb-0 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to GitHub Stars Program">GitHub Stars program</a></li>
                    </ul>
                  </div>
                </details>
              </li>

              <li class="border-bottom border-lg-bottom-0 mr-0 mr-lg-3">
                <a href="/marketplace" class="HeaderMenu-link no-underline py-3 d-block d-lg-inline-block" data-ga-click="(Logged out) Header, go to Marketplace">Marketplace</a>
              </li>

              <li class="d-block d-lg-flex flex-lg-nowrap flex-lg-items-center border-bottom border-lg-bottom-0 mr-0 mr-lg-3 edge-item-fix position-relative flex-wrap flex-justify-between d-flex flex-items-center ">
                <details class="HeaderMenu-details details-overlay details-reset width-full">
                  <summary class="HeaderMenu-summary HeaderMenu-link px-0 py-3 border-0 no-wrap d-block d-lg-inline-block">
                    Pricing
                    <svg x="0px" y="0px" viewBox="0 0 14 8" xml:space="preserve" fill="none" class="icon-chevon-down-mktg position-absolute position-lg-relative">
                       <path d="M1,1l6.2,6L13,1"></path>
                    </svg>
                  </summary>

                  <div class="dropdown-menu flex-auto rounded-1 bg-white px-0 pt-2 pb-4 mt-0 p-lg-4 position-relative position-lg-absolute left-0 left-lg-n4">
                    <a href="/pricing" class="pb-2 lh-condensed-ultra d-block link-gray-dark no-underline h5 Bump-link--hover" data-ga-click="(Logged out) Header, go to Pricing">Plans <span class="Bump-link-symbol float-right text-normal text-gray-light">&rarr;</span></a>

                    <ul class="list-style-none mb-3">
                      <li class="edge-item-fix"><a href="/pricing#feature-comparison" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Compare plans">Compare plans</a></li>
                      <li class="edge-item-fix"><a href="https://enterprise.github.com/contact" class="py-2 lh-condensed-ultra d-block link-gray no-underline f5" data-ga-click="(Logged out) Header, go to Contact Sales">Contact Sales</a></li>
                    </ul>

                    <ul class="list-style-none mb-0 border-lg-top pt-lg-3">
                      <li class="edge-item-fix"><a href="/nonprofit" class="py-2 lh-condensed-ultra d-block no-underline link-gray-dark no-underline h5 Bump-link--hover" data-ga-click="(Logged out) Header, go to Nonprofits">Nonprofit <span class="Bump-link-symbol float-right text-normal text-gray-light">&rarr;</span></a></li>
                      <li class="edge-item-fix"><a href="https://education.github.com" class="py-2 pb-0 lh-condensed-ultra d-block no-underline link-gray-dark no-underline h5 Bump-link--hover"  data-ga-click="(Logged out) Header, go to Education">Education <span class="Bump-link-symbol float-right text-normal text-gray-light">&rarr;</span></a></li>
                    </ul>
                  </div>
                </details>
              </li>
          </ul>
        </nav>

      <div class="d-lg-flex flex-items-center px-3 px-lg-0 text-center text-lg-left">
          <div class="d-lg-flex mb-3 mb-lg-0">
              <div hidden class="d-none">
</div>
<div class="header-search header-search-current js-header-search-current flex-auto  flex-self-stretch flex-md-self-auto mr-0 mr-md-3 mb-3 mb-md-0 scoped-search site-scoped-search js-site-search position-relative js-jump-to js-header-search-current-jump-to "
  role="combobox"
  aria-owns="jump-to-results"
  aria-label="Search or jump to"
  aria-haspopup="listbox"
  aria-expanded="false"
>
  <div class="position-relative">
    <!-- '"` --><!-- </textarea></xmp> --></option></form><form class="js-site-search-form" role="search" aria-label="Site" data-scope-type="Repository" data-scope-id="222721731" data-scoped-search-url="/adeiorio/nanoAOD-tools/search" data-unscoped-search-url="/search" action="/adeiorio/nanoAOD-tools/search" accept-charset="UTF-8" method="get">
      <label class="form-control input-sm header-search-wrapper p-0 header-search-wrapper-jump-to position-relative d-flex flex-justify-between flex-items-center js-chromeless-input-container">
        <input type="text"
          class="form-control input-sm header-search-input jump-to-field js-jump-to-field js-site-search-focus js-site-search-field is-clearable"
          data-hotkey="s,/"
          name="q"
          value=""
          placeholder="Search"
          data-unscoped-placeholder="Search GitHub"
          data-scoped-placeholder="Search"
          autocapitalize="off"
          aria-autocomplete="list"
          aria-controls="jump-to-results"
          aria-label="Search"
          data-jump-to-suggestions-path="/_graphql/GetSuggestedNavigationDestinations"
          spellcheck="false"
          autocomplete="off"
          >
          <input type="hidden" data-csrf="true" class="js-data-jump-to-suggestions-path-csrf" value="oC/vLiSf3Gcm7kx0sfNZwRpITXQRR5ui/u6LkiuPWaRKTCGLWCeIO+nH8iIUjgZWoGdCa5iiR0xNbHz7ZcsPRA==" />
          <input type="hidden" class="js-site-search-type-field" name="type" >
            <img src="https://github.githubassets.com/images/search-key-slash.svg" alt="" class="mr-2 header-search-key-slash">

            <div class="Box position-absolute overflow-hidden d-none jump-to-suggestions js-jump-to-suggestions-container">
              
<ul class="d-none js-jump-to-suggestions-template-container">
  

<li class="d-flex flex-justify-start flex-items-center p-0 f5 navigation-item js-navigation-item js-jump-to-suggestion" role="option">
  <a tabindex="-1" class="no-underline d-flex flex-auto flex-items-center jump-to-suggestions-path js-jump-to-suggestion-path js-navigation-open p-2" href="">
    <div class="jump-to-octicon js-jump-to-octicon flex-shrink-0 mr-2 text-center d-none">
      <svg height="16" width="16" class="octicon octicon-repo flex-shrink-0 js-jump-to-octicon-repo d-none" title="Repository" aria-label="Repository" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"></path></svg>
      <svg height="16" width="16" class="octicon octicon-project flex-shrink-0 js-jump-to-octicon-project d-none" title="Project" aria-label="Project" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M1.75 0A1.75 1.75 0 000 1.75v12.5C0 15.216.784 16 1.75 16h12.5A1.75 1.75 0 0016 14.25V1.75A1.75 1.75 0 0014.25 0H1.75zM1.5 1.75a.25.25 0 01.25-.25h12.5a.25.25 0 01.25.25v12.5a.25.25 0 01-.25.25H1.75a.25.25 0 01-.25-.25V1.75zM11.75 3a.75.75 0 00-.75.75v7.5a.75.75 0 001.5 0v-7.5a.75.75 0 00-.75-.75zm-8.25.75a.75.75 0 011.5 0v5.5a.75.75 0 01-1.5 0v-5.5zM8 3a.75.75 0 00-.75.75v3.5a.75.75 0 001.5 0v-3.5A.75.75 0 008 3z"></path></svg>
      <svg height="16" width="16" class="octicon octicon-search flex-shrink-0 js-jump-to-octicon-search d-none" title="Search" aria-label="Search" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M11.5 7a4.499 4.499 0 11-8.998 0A4.499 4.499 0 0111.5 7zm-.82 4.74a6 6 0 111.06-1.06l3.04 3.04a.75.75 0 11-1.06 1.06l-3.04-3.04z"></path></svg>
    </div>

    <img class="avatar mr-2 flex-shrink-0 js-jump-to-suggestion-avatar d-none" alt="" aria-label="Team" src="" width="28" height="28">

    <div class="jump-to-suggestion-name js-jump-to-suggestion-name flex-auto overflow-hidden text-left no-wrap css-truncate css-truncate-target">
    </div>

    <div class="border rounded-1 flex-shrink-0 bg-gray px-1 text-gray-light ml-1 f6 d-none js-jump-to-badge-search">
      <span class="js-jump-to-badge-search-text-default d-none" aria-label="in this repository">
        In this repository
      </span>
      <span class="js-jump-to-badge-search-text-global d-none" aria-label="in all of GitHub">
        All GitHub
      </span>
      <span aria-hidden="true" class="d-inline-block ml-1 v-align-middle">↵</span>
    </div>

    <div aria-hidden="true" class="border rounded-1 flex-shrink-0 bg-gray px-1 text-gray-light ml-1 f6 d-none d-on-nav-focus js-jump-to-badge-jump">
      Jump to
      <span class="d-inline-block ml-1 v-align-middle">↵</span>
    </div>
  </a>
</li>

</ul>

<ul class="d-none js-jump-to-no-results-template-container">
  <li class="d-flex flex-justify-center flex-items-center f5 d-none js-jump-to-suggestion p-2">
    <span class="text-gray">No suggested jump to results</span>
  </li>
</ul>

<ul id="jump-to-results" role="listbox" class="p-0 m-0 js-navigation-container jump-to-suggestions-results-container js-jump-to-suggestions-results-container">
  

<li class="d-flex flex-justify-start flex-items-center p-0 f5 navigation-item js-navigation-item js-jump-to-scoped-search d-none" role="option">
  <a tabindex="-1" class="no-underline d-flex flex-auto flex-items-center jump-to-suggestions-path js-jump-to-suggestion-path js-navigation-open p-2" href="">
    <div class="jump-to-octicon js-jump-to-octicon flex-shrink-0 mr-2 text-center d-none">
      <svg height="16" width="16" class="octicon octicon-repo flex-shrink-0 js-jump-to-octicon-repo d-none" title="Repository" aria-label="Repository" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"></path></svg>
      <svg height="16" width="16" class="octicon octicon-project flex-shrink-0 js-jump-to-octicon-project d-none" title="Project" aria-label="Project" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M1.75 0A1.75 1.75 0 000 1.75v12.5C0 15.216.784 16 1.75 16h12.5A1.75 1.75 0 0016 14.25V1.75A1.75 1.75 0 0014.25 0H1.75zM1.5 1.75a.25.25 0 01.25-.25h12.5a.25.25 0 01.25.25v12.5a.25.25 0 01-.25.25H1.75a.25.25 0 01-.25-.25V1.75zM11.75 3a.75.75 0 00-.75.75v7.5a.75.75 0 001.5 0v-7.5a.75.75 0 00-.75-.75zm-8.25.75a.75.75 0 011.5 0v5.5a.75.75 0 01-1.5 0v-5.5zM8 3a.75.75 0 00-.75.75v3.5a.75.75 0 001.5 0v-3.5A.75.75 0 008 3z"></path></svg>
      <svg height="16" width="16" class="octicon octicon-search flex-shrink-0 js-jump-to-octicon-search d-none" title="Search" aria-label="Search" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M11.5 7a4.499 4.499 0 11-8.998 0A4.499 4.499 0 0111.5 7zm-.82 4.74a6 6 0 111.06-1.06l3.04 3.04a.75.75 0 11-1.06 1.06l-3.04-3.04z"></path></svg>
    </div>

    <img class="avatar mr-2 flex-shrink-0 js-jump-to-suggestion-avatar d-none" alt="" aria-label="Team" src="" width="28" height="28">

    <div class="jump-to-suggestion-name js-jump-to-suggestion-name flex-auto overflow-hidden text-left no-wrap css-truncate css-truncate-target">
    </div>

    <div class="border rounded-1 flex-shrink-0 bg-gray px-1 text-gray-light ml-1 f6 d-none js-jump-to-badge-search">
      <span class="js-jump-to-badge-search-text-default d-none" aria-label="in this repository">
        In this repository
      </span>
      <span class="js-jump-to-badge-search-text-global d-none" aria-label="in all of GitHub">
        All GitHub
      </span>
      <span aria-hidden="true" class="d-inline-block ml-1 v-align-middle">↵</span>
    </div>

    <div aria-hidden="true" class="border rounded-1 flex-shrink-0 bg-gray px-1 text-gray-light ml-1 f6 d-none d-on-nav-focus js-jump-to-badge-jump">
      Jump to
      <span class="d-inline-block ml-1 v-align-middle">↵</span>
    </div>
  </a>
</li>

  

<li class="d-flex flex-justify-start flex-items-center p-0 f5 navigation-item js-navigation-item js-jump-to-global-search d-none" role="option">
  <a tabindex="-1" class="no-underline d-flex flex-auto flex-items-center jump-to-suggestions-path js-jump-to-suggestion-path js-navigation-open p-2" href="">
    <div class="jump-to-octicon js-jump-to-octicon flex-shrink-0 mr-2 text-center d-none">
      <svg height="16" width="16" class="octicon octicon-repo flex-shrink-0 js-jump-to-octicon-repo d-none" title="Repository" aria-label="Repository" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"></path></svg>
      <svg height="16" width="16" class="octicon octicon-project flex-shrink-0 js-jump-to-octicon-project d-none" title="Project" aria-label="Project" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M1.75 0A1.75 1.75 0 000 1.75v12.5C0 15.216.784 16 1.75 16h12.5A1.75 1.75 0 0016 14.25V1.75A1.75 1.75 0 0014.25 0H1.75zM1.5 1.75a.25.25 0 01.25-.25h12.5a.25.25 0 01.25.25v12.5a.25.25 0 01-.25.25H1.75a.25.25 0 01-.25-.25V1.75zM11.75 3a.75.75 0 00-.75.75v7.5a.75.75 0 001.5 0v-7.5a.75.75 0 00-.75-.75zm-8.25.75a.75.75 0 011.5 0v5.5a.75.75 0 01-1.5 0v-5.5zM8 3a.75.75 0 00-.75.75v3.5a.75.75 0 001.5 0v-3.5A.75.75 0 008 3z"></path></svg>
      <svg height="16" width="16" class="octicon octicon-search flex-shrink-0 js-jump-to-octicon-search d-none" title="Search" aria-label="Search" viewBox="0 0 16 16" version="1.1" role="img"><path fill-rule="evenodd" d="M11.5 7a4.499 4.499 0 11-8.998 0A4.499 4.499 0 0111.5 7zm-.82 4.74a6 6 0 111.06-1.06l3.04 3.04a.75.75 0 11-1.06 1.06l-3.04-3.04z"></path></svg>
    </div>

    <img class="avatar mr-2 flex-shrink-0 js-jump-to-suggestion-avatar d-none" alt="" aria-label="Team" src="" width="28" height="28">

    <div class="jump-to-suggestion-name js-jump-to-suggestion-name flex-auto overflow-hidden text-left no-wrap css-truncate css-truncate-target">
    </div>

    <div class="border rounded-1 flex-shrink-0 bg-gray px-1 text-gray-light ml-1 f6 d-none js-jump-to-badge-search">
      <span class="js-jump-to-badge-search-text-default d-none" aria-label="in this repository">
        In this repository
      </span>
      <span class="js-jump-to-badge-search-text-global d-none" aria-label="in all of GitHub">
        All GitHub
      </span>
      <span aria-hidden="true" class="d-inline-block ml-1 v-align-middle">↵</span>
    </div>

    <div aria-hidden="true" class="border rounded-1 flex-shrink-0 bg-gray px-1 text-gray-light ml-1 f6 d-none d-on-nav-focus js-jump-to-badge-jump">
      Jump to
      <span class="d-inline-block ml-1 v-align-middle">↵</span>
    </div>
  </a>
</li>


</ul>

            </div>
      </label>
</form>  </div>
</div>

          </div>

        <a href="/login?return_to=%2Fadeiorio%2FnanoAOD-tools%2Fblob%2Fmaster%2Fpython%2Fpostprocessing%2Fmakeplot.py"
          class="HeaderMenu-link no-underline mr-3"
          data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;site header menu&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;SIGN_UP&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="c223ffa1625e45b4e252f5b726e9f52459eb8bd23754dfa272da2af3e510d431"
          data-ga-click="(Logged out) Header, clicked Sign in, text:sign-in">
          Sign&nbsp;in
        </a>
            <a href="/join?ref_cta=Sign+up&amp;ref_loc=header+logged+out&amp;ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E%2Fblob%2Fshow&amp;source=header-repo&amp;source_repo=adeiorio%2FnanoAOD-tools"
              class="HeaderMenu-link d-inline-block no-underline border border-gray-dark rounded-1 px-2 py-1"
              data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;site header menu&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;SIGN_UP&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="c223ffa1625e45b4e252f5b726e9f52459eb8bd23754dfa272da2af3e510d431"
              data-ga-click="Sign up, click to sign up for account, ref_page:/&lt;user-name&gt;/&lt;repo-name&gt;/blob/show;ref_cta:Sign up;ref_loc:header logged out">
              Sign&nbsp;up
            </a>
      </div>
    </div>
  </div>
</header>

    </div>

  <div id="start-of-content" class="show-on-focus"></div>




    <div id="js-flash-container">


  <template class="js-flash-template">
    <div class="flash flash-full  {{ className }}">
  <div class=" px-2" >
    <button class="flash-close js-flash-close" type="button" aria-label="Dismiss this message">
      <svg class="octicon octicon-x" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"></path></svg>
    </button>
    
      <div>{{ message }}</div>

  </div>
</div>
  </template>
</div>


  

  <include-fragment class="js-notification-shelf-include-fragment" data-base-src="https://github.com/notifications/beta/shelf"></include-fragment>



  <div
    class="application-main "
    data-commit-hovercards-enabled
    data-discussion-hovercards-enabled
    data-issue-and-pr-hovercards-enabled
  >
        <div itemscope itemtype="http://schema.org/SoftwareSourceCode" class="">
    <main  >
      

    






  


  <div class="bg-gray-light pt-3 hide-full-screen mb-5">

      <div class="d-flex mb-3 px-3 px-md-4 px-lg-5">

        <div class="flex-auto min-width-0 width-fit mr-3">
            <h1 class=" d-flex flex-wrap flex-items-center break-word f3 text-normal">
    <svg class="octicon octicon-repo-forked text-gray" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"></path></svg>
  <span class="author ml-2 flex-self-stretch" itemprop="author">
    <a class="url fn" rel="author" data-hovercard-type="user" data-hovercard-url="/users/adeiorio/hovercard" data-octo-click="hovercard-link-click" data-octo-dimensions="link_type:self" href="/adeiorio">adeiorio</a>
  </span>
  <span class="mx-1 flex-self-stretch">/</span>
  <strong itemprop="name" class="mr-2 flex-self-stretch">
    <a data-pjax="#js-repo-pjax-container" href="/adeiorio/nanoAOD-tools">nanoAOD-tools</a>
  </strong>
  
</h1>

  <span class="text-small lh-condensed-ultra no-wrap mt-1" data-repository-hovercards-enabled>
    forked from <a data-hovercard-type="repository" data-hovercard-url="/cms-nanoAOD/nanoAOD-tools/hovercard" href="/cms-nanoAOD/nanoAOD-tools">cms-nanoAOD/nanoAOD-tools</a>
  </span>

        </div>

          <ul class="pagehead-actions flex-shrink-0 d-none d-md-inline" style="padding: 2px 0;">

  <li>
        <a class="tooltipped tooltipped-s btn btn-sm btn-with-count" aria-label="You must be signed in to watch a repository" rel="nofollow" data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;notification subscription menu watch&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;LOG_IN&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="084fb26e2a6bdb86aca52414457584eca06316f811714d675d353fc8e54c5064" href="/login?return_to=%2Fadeiorio%2FnanoAOD-tools">
    <svg height="16" class="octicon octicon-eye" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M1.679 7.932c.412-.621 1.242-1.75 2.366-2.717C5.175 4.242 6.527 3.5 8 3.5c1.473 0 2.824.742 3.955 1.715 1.124.967 1.954 2.096 2.366 2.717a.119.119 0 010 .136c-.412.621-1.242 1.75-2.366 2.717C10.825 11.758 9.473 12.5 8 12.5c-1.473 0-2.824-.742-3.955-1.715C2.92 9.818 2.09 8.69 1.679 8.068a.119.119 0 010-.136zM8 2c-1.981 0-3.67.992-4.933 2.078C1.797 5.169.88 6.423.43 7.1a1.619 1.619 0 000 1.798c.45.678 1.367 1.932 2.637 3.024C4.329 13.008 6.019 14 8 14c1.981 0 3.67-.992 4.933-2.078 1.27-1.091 2.187-2.345 2.637-3.023a1.619 1.619 0 000-1.798c-.45-.678-1.367-1.932-2.637-3.023C11.671 2.992 9.981 2 8 2zm0 8a2 2 0 100-4 2 2 0 000 4z"></path></svg>
    Watch
</a>    <a class="social-count" href="/adeiorio/nanoAOD-tools/watchers"
       aria-label="0 users are watching this repository">
      0
    </a>

  </li>

  <li>
          <a class="btn btn-sm btn-with-count  tooltipped tooltipped-s" aria-label="You must be signed in to star a repository" rel="nofollow" data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;star button&quot;,&quot;repository_id&quot;:222721731,&quot;auth_type&quot;:&quot;LOG_IN&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="acf2c65ab8f650ab9e899789c102c5b5421c16190e6758ab1c2cfa0ce4c9afb9" href="/login?return_to=%2Fadeiorio%2FnanoAOD-tools">
      <svg vertical_align="text_bottom" height="16" class="octicon octicon-star v-align-text-bottom" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"></path></svg>
      Star
</a>
    <a class="social-count js-social-count" href="/adeiorio/nanoAOD-tools/stargazers"
      aria-label="0 users starred this repository">
      0
    </a>

  </li>

  <li>
        <a class="btn btn-sm btn-with-count tooltipped tooltipped-s" aria-label="You must be signed in to fork a repository" rel="nofollow" data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;repo details fork button&quot;,&quot;repository_id&quot;:222721731,&quot;auth_type&quot;:&quot;LOG_IN&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="4c61133d809413465347d898cb4f256f0793abc1717db96aa1cae39d1a0d7da7" href="/login?return_to=%2Fadeiorio%2FnanoAOD-tools">
          <svg class="octicon octicon-repo-forked" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"></path></svg>
          Fork
</a>
      <a href="/adeiorio/nanoAOD-tools/network/members" class="social-count"
         aria-label="158 users forked this repository">
        158
      </a>
  </li>
</ul>

      </div>
        
<nav aria-label="Repository" data-pjax="#js-repo-pjax-container" class="js-repo-nav js-sidenav-container-pjax js-responsive-underlinenav overflow-hidden UnderlineNav px-3 px-md-4 px-lg-5 bg-gray-light">
  <ul class="UnderlineNav-body list-style-none ">
          <li class="d-flex">
        <a class="js-selected-navigation-item selected UnderlineNav-item hx_underlinenav-item no-wrap js-responsive-underlinenav-item" data-tab-item="code-tab" data-hotkey="g c" data-ga-click="Repository, Navigation click, Code tab" aria-current="page" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches repo_packages repo_deployments /adeiorio/nanoAOD-tools" href="/adeiorio/nanoAOD-tools">
              <svg classes="UnderlineNav-octicon" display="none inline" height="16" class="octicon octicon-code UnderlineNav-octicon d-none d-sm-inline" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M4.72 3.22a.75.75 0 011.06 1.06L2.06 8l3.72 3.72a.75.75 0 11-1.06 1.06L.47 8.53a.75.75 0 010-1.06l4.25-4.25zm6.56 0a.75.75 0 10-1.06 1.06L13.94 8l-3.72 3.72a.75.75 0 101.06 1.06l4.25-4.25a.75.75 0 000-1.06l-4.25-4.25z"></path></svg>
            <span data-content="Code">Code</span>
              <span title="Not available" class="Counter "></span>
</a>      </li>
      <li class="d-flex">
        <a class="js-selected-navigation-item UnderlineNav-item hx_underlinenav-item no-wrap js-responsive-underlinenav-item" data-tab-item="pull-requests-tab" data-hotkey="g p" data-ga-click="Repository, Navigation click, Pull requests tab" data-selected-links="repo_pulls checks /adeiorio/nanoAOD-tools/pulls" href="/adeiorio/nanoAOD-tools/pulls">
              <svg classes="UnderlineNav-octicon" display="none inline" height="16" class="octicon octicon-git-pull-request UnderlineNav-octicon d-none d-sm-inline" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z"></path></svg>
            <span data-content="Pull requests">Pull requests</span>
              <span title="0" hidden="hidden" class="Counter ">0</span>
</a>      </li>
      <li class="d-flex">
        <a class="js-selected-navigation-item UnderlineNav-item hx_underlinenav-item no-wrap js-responsive-underlinenav-item" data-tab-item="actions-tab" data-hotkey="g a" data-ga-click="Repository, Navigation click, Actions tab" data-selected-links="repo_actions /adeiorio/nanoAOD-tools/actions" href="/adeiorio/nanoAOD-tools/actions">
              <svg classes="UnderlineNav-octicon" display="none inline" height="16" class="octicon octicon-play UnderlineNav-octicon d-none d-sm-inline" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0zM8 0a8 8 0 100 16A8 8 0 008 0zM6.379 5.227A.25.25 0 006 5.442v5.117a.25.25 0 00.379.214l4.264-2.559a.25.25 0 000-.428L6.379 5.227z"></path></svg>
            <span data-content="Actions">Actions</span>
              <span title="Not available" class="Counter "></span>
</a>      </li>
      <li class="d-flex">
        <a class="js-selected-navigation-item UnderlineNav-item hx_underlinenav-item no-wrap js-responsive-underlinenav-item" data-tab-item="projects-tab" data-hotkey="g b" data-ga-click="Repository, Navigation click, Projects tab" data-selected-links="repo_projects new_repo_project repo_project /adeiorio/nanoAOD-tools/projects" href="/adeiorio/nanoAOD-tools/projects">
              <svg classes="UnderlineNav-octicon" display="none inline" height="16" class="octicon octicon-project UnderlineNav-octicon d-none d-sm-inline" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M1.75 0A1.75 1.75 0 000 1.75v12.5C0 15.216.784 16 1.75 16h12.5A1.75 1.75 0 0016 14.25V1.75A1.75 1.75 0 0014.25 0H1.75zM1.5 1.75a.25.25 0 01.25-.25h12.5a.25.25 0 01.25.25v12.5a.25.25 0 01-.25.25H1.75a.25.25 0 01-.25-.25V1.75zM11.75 3a.75.75 0 00-.75.75v7.5a.75.75 0 001.5 0v-7.5a.75.75 0 00-.75-.75zm-8.25.75a.75.75 0 011.5 0v5.5a.75.75 0 01-1.5 0v-5.5zM8 3a.75.75 0 00-.75.75v3.5a.75.75 0 001.5 0v-3.5A.75.75 0 008 3z"></path></svg>
            <span data-content="Projects">Projects</span>
              <span title="0" hidden="hidden" class="Counter ">0</span>
</a>      </li>
      <li class="d-flex">
        <a class="js-selected-navigation-item UnderlineNav-item hx_underlinenav-item no-wrap js-responsive-underlinenav-item" data-tab-item="security-tab" data-hotkey="g s" data-ga-click="Repository, Navigation click, Security tab" data-selected-links="security overview alerts policy token_scanning code_scanning /adeiorio/nanoAOD-tools/security" href="/adeiorio/nanoAOD-tools/security">
              <svg classes="UnderlineNav-octicon" display="none inline" height="16" class="octicon octicon-shield UnderlineNav-octicon d-none d-sm-inline" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.467.133a1.75 1.75 0 011.066 0l5.25 1.68A1.75 1.75 0 0115 3.48V7c0 1.566-.32 3.182-1.303 4.682-.983 1.498-2.585 2.813-5.032 3.855a1.7 1.7 0 01-1.33 0c-2.447-1.042-4.049-2.357-5.032-3.855C1.32 10.182 1 8.566 1 7V3.48a1.75 1.75 0 011.217-1.667l5.25-1.68zm.61 1.429a.25.25 0 00-.153 0l-5.25 1.68a.25.25 0 00-.174.238V7c0 1.358.275 2.666 1.057 3.86.784 1.194 2.121 2.34 4.366 3.297a.2.2 0 00.154 0c2.245-.956 3.582-2.104 4.366-3.298C13.225 9.666 13.5 8.36 13.5 7V3.48a.25.25 0 00-.174-.237l-5.25-1.68zM9 10.5a1 1 0 11-2 0 1 1 0 012 0zm-.25-5.75a.75.75 0 10-1.5 0v3a.75.75 0 001.5 0v-3z"></path></svg>
            <span data-content="Security">Security</span>
              <include-fragment src="/adeiorio/nanoAOD-tools/security/overall-count" accept="text/fragment+html"></include-fragment>
</a>      </li>
      <li class="d-flex">
        <a class="js-selected-navigation-item UnderlineNav-item hx_underlinenav-item no-wrap js-responsive-underlinenav-item" data-tab-item="insights-tab" data-ga-click="Repository, Navigation click, Insights tab" data-selected-links="repo_graphs repo_contributors dependency_graph dependabot_updates pulse people /adeiorio/nanoAOD-tools/pulse" href="/adeiorio/nanoAOD-tools/pulse">
              <svg classes="UnderlineNav-octicon" display="none inline" height="16" class="octicon octicon-graph UnderlineNav-octicon d-none d-sm-inline" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M1.5 1.75a.75.75 0 00-1.5 0v12.5c0 .414.336.75.75.75h14.5a.75.75 0 000-1.5H1.5V1.75zm14.28 2.53a.75.75 0 00-1.06-1.06L10 7.94 7.53 5.47a.75.75 0 00-1.06 0L3.22 8.72a.75.75 0 001.06 1.06L7 7.06l2.47 2.47a.75.75 0 001.06 0l5.25-5.25z"></path></svg>
            <span data-content="Insights">Insights</span>
              <span title="Not available" class="Counter "></span>
</a>      </li>

</ul>        <div class="position-absolute right-0 pr-3 pr-md-4 pr-lg-5 js-responsive-underlinenav-overflow" style="visibility:hidden;">
      <details class="details-overlay details-reset position-relative">
  <summary role="button">
    <div class="UnderlineNav-item mr-0 border-0">
            <svg class="octicon octicon-kebab-horizontal" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M8 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM1.5 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm13 0a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path></svg>
            <span class="sr-only">More</span>
          </div>
</summary>  <div>
    <details-menu role="menu" class="dropdown-menu dropdown-menu-sw ">
  
            <ul>
                <li data-menu-item="code-tab" hidden>
                  <a role="menuitem" class="js-selected-navigation-item dropdown-item" data-selected-links=" /adeiorio/nanoAOD-tools" href="/adeiorio/nanoAOD-tools">
                    Code
</a>                </li>
                <li data-menu-item="pull-requests-tab" hidden>
                  <a role="menuitem" class="js-selected-navigation-item dropdown-item" data-selected-links=" /adeiorio/nanoAOD-tools/pulls" href="/adeiorio/nanoAOD-tools/pulls">
                    Pull requests
</a>                </li>
                <li data-menu-item="actions-tab" hidden>
                  <a role="menuitem" class="js-selected-navigation-item dropdown-item" data-selected-links=" /adeiorio/nanoAOD-tools/actions" href="/adeiorio/nanoAOD-tools/actions">
                    Actions
</a>                </li>
                <li data-menu-item="projects-tab" hidden>
                  <a role="menuitem" class="js-selected-navigation-item dropdown-item" data-selected-links=" /adeiorio/nanoAOD-tools/projects" href="/adeiorio/nanoAOD-tools/projects">
                    Projects
</a>                </li>
                <li data-menu-item="security-tab" hidden>
                  <a role="menuitem" class="js-selected-navigation-item dropdown-item" data-selected-links=" /adeiorio/nanoAOD-tools/security" href="/adeiorio/nanoAOD-tools/security">
                    Security
</a>                </li>
                <li data-menu-item="insights-tab" hidden>
                  <a role="menuitem" class="js-selected-navigation-item dropdown-item" data-selected-links=" /adeiorio/nanoAOD-tools/pulse" href="/adeiorio/nanoAOD-tools/pulse">
                    Insights
</a>                </li>
            </ul>

</details-menu>
</div></details>    </div>

</nav>
  </div>

<div class="container-xl clearfix new-discussion-timeline  px-3 px-md-4 px-lg-5">
  <div class="repository-content " >

    
      
  


    <a class="d-none js-permalink-shortcut" data-hotkey="y" href="/adeiorio/nanoAOD-tools/blob/61fb7b8ec6e08ba888855132a00563f6ef7b22cc/python/postprocessing/makeplot.py">Permalink</a>

    <!-- blob contrib key: blob_contributors:v22:06b554e1096022ffc4050555c694a3778ee6f56b4b4790d6e1779b4e6a9c8973 -->
      <signup-prompt class="signup-prompt-bg rounded-1" data-prompt="signup" hidden>
    <div class="signup-prompt p-4 text-center mb-4 rounded-1">
      <div class="position-relative">
        <button
          type="button"
          class="position-absolute top-0 right-0 btn-link link-gray"
          data-action="click:signup-prompt#dismiss"
          data-ga-click="(Logged out) Sign up prompt, clicked Dismiss, text:dismiss"
        >
          Dismiss
        </button>
        <h3 class="pt-2">Join GitHub today</h3>
        <p class="col-6 mx-auto">GitHub is home to over 50 million developers working together to host and review code, manage projects, and build software together.</p>
        <a class="btn btn-primary" data-ga-click="(Logged out) Sign up prompt, clicked Sign up, text:sign-up" data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;files signup prompt&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;SIGN_UP&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="da94325c32695d3cc77583fd8cef4294fd6b2745af837a3ba8bae38cb3f71454" href="/join?source=prompt-blob-show&amp;source_repo=adeiorio%2FnanoAOD-tools">Sign up</a>
      </div>
    </div>
  </signup-prompt>


    <div class="d-flex flex-items-start flex-shrink-0 pb-3 flex-wrap flex-md-nowrap flex-justify-between flex-md-justify-start">
      
<div class="position-relative">
  <details class="details-reset details-overlay mr-0 mb-0 " id="branch-select-menu">
    <summary class="btn css-truncate"
            data-hotkey="w"
            title="Switch branches or tags">
      <svg text="gray" height="16" class="octicon octicon-git-branch text-gray" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M11.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122V6A2.5 2.5 0 0110 8.5H6a1 1 0 00-1 1v1.128a2.251 2.251 0 11-1.5 0V5.372a2.25 2.25 0 111.5 0v1.836A2.492 2.492 0 016 7h4a1 1 0 001-1v-.628A2.25 2.25 0 019.5 3.25zM4.25 12a.75.75 0 100 1.5.75.75 0 000-1.5zM3.5 3.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0z"></path></svg>
      <span class="css-truncate-target" data-menu-button>master</span>
      <span class="dropdown-caret"></span>
    </summary>

    <details-menu class="SelectMenu SelectMenu--hasFilter" src="/adeiorio/nanoAOD-tools/refs/master/python/postprocessing/makeplot.py?source_action=show&amp;source_controller=blob" preload>
      <div class="SelectMenu-modal">
        <include-fragment class="SelectMenu-loading" aria-label="Menu is loading">
          <svg class="octicon octicon-octoface anim-pulse" height="32" viewBox="0 0 24 24" version="1.1" width="32" aria-hidden="true"><path d="M7.75 11c-.69 0-1.25.56-1.25 1.25v1.5a1.25 1.25 0 102.5 0v-1.5C9 11.56 8.44 11 7.75 11zm1.27 4.5a.469.469 0 01.48-.5h5a.47.47 0 01.48.5c-.116 1.316-.759 2.5-2.98 2.5s-2.864-1.184-2.98-2.5zm7.23-4.5c-.69 0-1.25.56-1.25 1.25v1.5a1.25 1.25 0 102.5 0v-1.5c0-.69-.56-1.25-1.25-1.25z"></path><path fill-rule="evenodd" d="M21.255 3.82a1.725 1.725 0 00-2.141-1.195c-.557.16-1.406.44-2.264.866-.78.386-1.647.93-2.293 1.677A18.442 18.442 0 0012 5c-.93 0-1.784.059-2.569.17-.645-.74-1.505-1.28-2.28-1.664a13.876 13.876 0 00-2.265-.866 1.725 1.725 0 00-2.141 1.196 23.645 23.645 0 00-.69 3.292c-.125.97-.191 2.07-.066 3.112C1.254 11.882 1 13.734 1 15.527 1 19.915 3.13 23 12 23c8.87 0 11-3.053 11-7.473 0-1.794-.255-3.647-.99-5.29.127-1.046.06-2.15-.066-3.125a23.652 23.652 0 00-.689-3.292zM20.5 14c.5 3.5-1.5 6.5-8.5 6.5s-9-3-8.5-6.5c.583-4 3-6 8.5-6s7.928 2 8.5 6z"></path></svg>
        </include-fragment>
      </div>
    </details-menu>
  </details>

</div>

      <h2 id="blob-path" class="breadcrumb flex-auto min-width-0 text-normal mx-0 mx-md-3 width-full width-md-auto flex-order-1 flex-md-order-none mt-3 mt-md-0">
        <span class="js-repo-root text-bold"><span class="js-path-segment d-inline-block wb-break-all"><a data-pjax="true" href="/adeiorio/nanoAOD-tools"><span>nanoAOD-tools</span></a></span></span><span class="separator">/</span><span class="js-path-segment d-inline-block wb-break-all"><a data-pjax="true" href="/adeiorio/nanoAOD-tools/tree/master/python"><span>python</span></a></span><span class="separator">/</span><span class="js-path-segment d-inline-block wb-break-all"><a data-pjax="true" href="/adeiorio/nanoAOD-tools/tree/master/python/postprocessing"><span>postprocessing</span></a></span><span class="separator">/</span><strong class="final-path">makeplot.py</strong>
          <span class="separator">/</span><details class="details-reset details-overlay d-inline" id="jumpto-symbol-select-menu">
  <summary class="btn-link link-gray css-truncate" aria-haspopup="true" data-hotkey="r" data-hydro-click="{&quot;event_type&quot;:&quot;code_navigation.click_on_blob_definitions&quot;,&quot;payload&quot;:{&quot;action&quot;:&quot;click_on_blob_definitions&quot;,&quot;repository_id&quot;:222721731,&quot;ref&quot;:&quot;master&quot;,&quot;language&quot;:&quot;Python&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="75969820d0779c3c6a8e74ad844e014a5c8fc2797c215cf2c51a0286b6570f1c">
      <svg class="octicon octicon-code" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4.72 3.22a.75.75 0 011.06 1.06L2.06 8l3.72 3.72a.75.75 0 11-1.06 1.06L.47 8.53a.75.75 0 010-1.06l4.25-4.25zm6.56 0a.75.75 0 10-1.06 1.06L13.94 8l-3.72 3.72a.75.75 0 101.06 1.06l4.25-4.25a.75.75 0 000-1.06l-4.25-4.25z"></path></svg>
    <span data-menu-button>Jump to</span>
    <span class="dropdown-caret"></span>
  </summary>
  <details-menu class="SelectMenu SelectMenu--hasFilter" role="menu">
    <div class="SelectMenu-modal">
      <header class="SelectMenu-header">
        <span class="SelectMenu-title">Code definitions</span>
        <button class="SelectMenu-closeButton" type="button" data-toggle-for="jumpto-symbol-select-menu">
          <svg aria-label="Close menu" class="octicon octicon-x" viewBox="0 0 16 16" version="1.1" width="16" height="16" role="img"><path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"></path></svg>
        </button>
      </header>
      <div class="SelectMenu-list">
          <div class="SelectMenu-blankslate">
            <p class="mb-0 text-gray">
              No definitions found in this file.
            </p>
          </div>
        <div data-filterable-for="jumpto-symbols-filter-field" data-filterable-type="substring">
        </div>
      </div>
      <footer class="SelectMenu-footer">
        <div class="d-flex flex-justify-between">
          Code navigation not available for this commit
          <svg class="octicon octicon-dot-fill text-light-gray" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8z"></path></svg>
        </div>
      </footer>
    </div>
  </details-menu>
</details>

      </h2>
      <a href="/adeiorio/nanoAOD-tools/find/master"
            class="js-pjax-capture-input btn mr-2 d-none d-md-block"
            data-pjax
            data-hotkey="t">
        Go to file
      </a>

      <details id="blob-more-options-details" class="details-overlay details-reset position-relative">
  <summary role="button">
    <svg aria-label="More options" height="16" class="octicon octicon-kebab-horizontal" viewBox="0 0 16 16" version="1.1" width="16" role="img"><path d="M8 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM1.5 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm13 0a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path></svg>
</summary>  <div>
    <ul class="dropdown-menu dropdown-menu-sw">
            <li class="d-block d-md-none">
              <a class="dropdown-item d-flex flex-items-baseline" data-hydro-click="{&quot;event_type&quot;:&quot;repository.click&quot;,&quot;payload&quot;:{&quot;target&quot;:&quot;FIND_FILE_BUTTON&quot;,&quot;repository_id&quot;:222721731,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="6040f9e68b8bea2ce85fc37bfe96cb55933bc1a5a052dbeb0a6f05a80c70561c" data-ga-click="Repository, find file, location:repo overview" data-hotkey="t" data-pjax="true" href="/adeiorio/nanoAOD-tools/find/master">
                <span class="flex-auto">Go to file</span>
                <span class="text-small text-gray" aria-hidden="true">T</span>
</a>            </li>
            <li data-toggle-for="blob-more-options-details">
              <button type="button" data-toggle-for="jumpto-line-details-dialog" class="btn-link dropdown-item">
                <span class="d-flex flex-items-baseline">
                  <span class="flex-auto">Go to line</span>
                  <span class="text-small text-gray" aria-hidden="true">L</span>
                </span>
              </button>
            </li>
            <li data-toggle-for="blob-more-options-details">
              <button type="button" data-toggle-for="jumpto-symbol-select-menu" class="btn-link dropdown-item">
                <span class="d-flex flex-items-baseline">
                  <span class="flex-auto">Go to definition</span>
                  <span class="text-small text-gray" aria-hidden="true">R</span>
                </span>
              </button>
            </li>
            <li class="dropdown-divider" role="none"></li>
            <li>
              <clipboard-copy value="python/postprocessing/makeplot.py" class="dropdown-item cursor-pointer" data-toggle-for="blob-more-options-details">
                Copy path
              </clipboard-copy>
            </li>
          </ul>
</div></details>    </div>



    <div class="Box d-flex flex-column flex-shrink-0 mb-3">
      
  <div class="Box-header Box-header--blue Details js-details-container">
      <div class="d-flex flex-items-center">
        <span class="flex-shrink-0 ml-n1 mr-n1 mt-n1 mb-n1">
          <a rel="author" data-skip-pjax="true" data-hovercard-type="user" data-hovercard-url="/users/adeiorio/hovercard" data-octo-click="hovercard-link-click" data-octo-dimensions="link_type:self" href="/adeiorio"><img class="avatar avatar-user" src="https://avatars0.githubusercontent.com/u/28299733?s=48&amp;v=4" width="24" height="24" alt="@adeiorio" /></a>
        </span>
        <div class="flex-1 d-flex flex-items-center ml-3 min-width-0">
          <div class="css-truncate css-truncate-overflow">
            <a class="text-bold link-gray-dark" rel="author" data-hovercard-type="user" data-hovercard-url="/users/adeiorio/hovercard" data-octo-click="hovercard-link-click" data-octo-dimensions="link_type:self" href="/adeiorio">adeiorio</a>

              <span>
                <a data-pjax="true" title="Merge branch &#39;master&#39; into master" class="link-gray" href="/adeiorio/nanoAOD-tools/commit/fb993e23e5821cf84d01e119cbc4decfc51da7d1">Merge branch 'master' into master</a>
              </span>
          </div>


          <span class="ml-2">
            <include-fragment accept="text/fragment+html" src="/adeiorio/nanoAOD-tools/commit/fb993e23e5821cf84d01e119cbc4decfc51da7d1/rollup?direction=e" class="d-inline"></include-fragment>
          </span>
        </div>
        <div class="ml-3 d-flex flex-shrink-0 flex-items-center flex-justify-end text-gray no-wrap">
          <span class="d-none d-md-inline">
            <span>Latest commit</span>
            <a class="text-small text-mono link-gray" href="/adeiorio/nanoAOD-tools/commit/fb993e23e5821cf84d01e119cbc4decfc51da7d1" data-pjax>fb993e2</a>
            <span itemprop="dateModified"><relative-time datetime="2020-09-15T07:58:42Z" class="no-wrap">Sep 15, 2020</relative-time></span>
          </span>

          <a data-pjax href="/adeiorio/nanoAOD-tools/commits/master/python/postprocessing/makeplot.py" class="ml-3 no-wrap link-gray-dark no-underline">
            <svg text="gray" height="16" class="octicon octicon-history text-gray" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M1.643 3.143L.427 1.927A.25.25 0 000 2.104V5.75c0 .138.112.25.25.25h3.646a.25.25 0 00.177-.427L2.715 4.215a6.5 6.5 0 11-1.18 4.458.75.75 0 10-1.493.154 8.001 8.001 0 101.6-5.684zM7.75 4a.75.75 0 01.75.75v2.992l2.028.812a.75.75 0 01-.557 1.392l-2.5-1A.75.75 0 017 8.25v-3.5A.75.75 0 017.75 4z"></path></svg>
            <span class="d-none d-sm-inline">
              <strong>History</strong>
            </span>
          </a>
        </div>
      </div>

  </div>

  <div class="Box-body d-flex flex-items-center flex-auto border-bottom-0 flex-wrap" >
    <details class="details-reset details-overlay details-overlay-dark lh-default text-gray-dark float-left mr-3" id="blob_contributors_box">
      <summary class="link-gray-dark">
        <svg text="gray" height="16" class="octicon octicon-people text-gray" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill-rule="evenodd" d="M5.5 3.5a2 2 0 100 4 2 2 0 000-4zM2 5.5a3.5 3.5 0 115.898 2.549 5.507 5.507 0 013.034 4.084.75.75 0 11-1.482.235 4.001 4.001 0 00-7.9 0 .75.75 0 01-1.482-.236A5.507 5.507 0 013.102 8.05 3.49 3.49 0 012 5.5zM11 4a.75.75 0 100 1.5 1.5 1.5 0 01.666 2.844.75.75 0 00-.416.672v.352a.75.75 0 00.574.73c1.2.289 2.162 1.2 2.522 2.372a.75.75 0 101.434-.44 5.01 5.01 0 00-2.56-3.012A3 3 0 0011 4z"></path></svg>
        <strong>2</strong>
        
        contributors
      </summary>
      <details-dialog
        class="Box Box--overlay d-flex flex-column anim-fade-in fast"
        aria-label="Users who have contributed to this file"
        src="/adeiorio/nanoAOD-tools/contributors-list/master/python/postprocessing/makeplot.py" preload>
        <div class="Box-header">
          <button class="Box-btn-octicon btn-octicon float-right" type="button" aria-label="Close dialog" data-close-dialog>
            <svg class="octicon octicon-x" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"></path></svg>
          </button>
          <h3 class="Box-title">
            Users who have contributed to this file
          </h3>
        </div>
        <include-fragment class="octocat-spinner my-3" aria-label="Loading..."></include-fragment>
      </details-dialog>
    </details>
      <span class="">
    <a class="avatar-link" data-hovercard-type="user" data-hovercard-url="/users/anpicci/hovercard" data-octo-click="hovercard-link-click" data-octo-dimensions="link_type:self" href="/adeiorio/nanoAOD-tools/commits/master/python/postprocessing/makeplot.py?author=anpicci">
      <img class="avatar mr-2 avatar-user" src="https://avatars0.githubusercontent.com/u/44297061?s=48&amp;v=4" width="24" height="24" alt="@anpicci" /> 
</a>    <a class="avatar-link" data-hovercard-type="user" data-hovercard-url="/users/adeiorio/hovercard" data-octo-click="hovercard-link-click" data-octo-dimensions="link_type:self" href="/adeiorio/nanoAOD-tools/commits/master/python/postprocessing/makeplot.py?author=adeiorio">
      <img class="avatar mr-2 avatar-user" src="https://avatars0.githubusercontent.com/u/28299733?s=48&amp;v=4" width="24" height="24" alt="@adeiorio" /> 
</a>
</span>

  </div>
    </div>






    <div class="Box mt-3 position-relative
      ">
      
<div class="Box-header py-2 d-flex flex-column flex-shrink-0 flex-md-row flex-md-items-center">
  <div class="text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0">

      702 lines (663 sloc)
      <span class="file-info-divider"></span>
    41.2 KB
  </div>

  <div class="d-flex py-1 py-md-0 flex-auto flex-order-1 flex-md-order-2 flex-sm-grow-0 flex-justify-between">

    <div class="BtnGroup">
      <a href="/adeiorio/nanoAOD-tools/raw/master/python/postprocessing/makeplot.py" id="raw-url" role="button" class="btn btn-sm BtnGroup-item ">Raw</a>
        <a href="/adeiorio/nanoAOD-tools/blame/master/python/postprocessing/makeplot.py" data-hotkey="b" role="button" class="btn js-update-url-with-hash btn-sm BtnGroup-item ">Blame</a>
    </div>

    <div>
          <a class="btn-octicon tooltipped tooltipped-nw js-remove-unless-platform"
             data-platforms="windows,mac"
             href="https://desktop.github.com"
             aria-label="Open this file in GitHub Desktop"
             data-ga-click="Repository, open with desktop">
              <svg class="octicon octicon-device-desktop" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M1.75 2.5h12.5a.25.25 0 01.25.25v7.5a.25.25 0 01-.25.25H1.75a.25.25 0 01-.25-.25v-7.5a.25.25 0 01.25-.25zM14.25 1H1.75A1.75 1.75 0 000 2.75v7.5C0 11.216.784 12 1.75 12h3.727c-.1 1.041-.52 1.872-1.292 2.757A.75.75 0 004.75 16h6.5a.75.75 0 00.565-1.243c-.772-.885-1.193-1.716-1.292-2.757h3.727A1.75 1.75 0 0016 10.25v-7.5A1.75 1.75 0 0014.25 1zM9.018 12H6.982a5.72 5.72 0 01-.765 2.5h3.566a5.72 5.72 0 01-.765-2.5z"></path></svg>
          </a>

          <a href="/login?return_to=%2Fadeiorio%2FnanoAOD-tools%2Fblob%2Fmaster%2Fpython%2Fpostprocessing%2Fmakeplot.py" class="btn-octicon disabled tooltipped tooltipped-nw"
            aria-label="You must be signed in to make or propose changes">
            <svg class="octicon octicon-pencil" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M11.013 1.427a1.75 1.75 0 012.474 0l1.086 1.086a1.75 1.75 0 010 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 01-.927-.928l.929-3.25a1.75 1.75 0 01.445-.758l8.61-8.61zm1.414 1.06a.25.25 0 00-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 000-.354l-1.086-1.086zM11.189 6.25L9.75 4.81l-6.286 6.287a.25.25 0 00-.064.108l-.558 1.953 1.953-.558a.249.249 0 00.108-.064l6.286-6.286z"></path></svg>
          </a>
          <a href="/login?return_to=%2Fadeiorio%2FnanoAOD-tools%2Fblob%2Fmaster%2Fpython%2Fpostprocessing%2Fmakeplot.py" class="btn-octicon btn-octicon-danger disabled tooltipped tooltipped-nw"
            aria-label="You must be signed in to make or propose changes">
            <svg class="octicon octicon-trashcan" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M6.5 1.75a.25.25 0 01.25-.25h2.5a.25.25 0 01.25.25V3h-3V1.75zm4.5 0V3h2.25a.75.75 0 010 1.5H2.75a.75.75 0 010-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75zM4.496 6.675a.75.75 0 10-1.492.15l.66 6.6A1.75 1.75 0 005.405 15h5.19c.9 0 1.652-.681 1.741-1.576l.66-6.6a.75.75 0 00-1.492-.149l-.66 6.6a.25.25 0 01-.249.225h-5.19a.25.25 0 01-.249-.225l-.66-6.6z"></path></svg>
          </a>
    </div>
  </div>
</div>



      

  <div itemprop="text" class="Box-body p-0 blob-wrapper data type-python  gist-border-0">
      
<table class="highlight tab-size js-file-line-container" data-tab-size="8" data-paste-markdown-skip>
      <tr>
        <td id="L1" class="blob-num js-line-number" data-line-number="1"></td>
        <td id="LC1" class="blob-code blob-code-inner js-file-line"><span class=pl-k>import</span> <span class=pl-s1>os</span>, <span class=pl-s1>commands</span></td>
      </tr>
      <tr>
        <td id="L2" class="blob-num js-line-number" data-line-number="2"></td>
        <td id="LC2" class="blob-code blob-code-inner js-file-line"><span class=pl-k>import</span> <span class=pl-s1>sys</span></td>
      </tr>
      <tr>
        <td id="L3" class="blob-num js-line-number" data-line-number="3"></td>
        <td id="LC3" class="blob-code blob-code-inner js-file-line"><span class=pl-k>import</span> <span class=pl-s1>optparse</span></td>
      </tr>
      <tr>
        <td id="L4" class="blob-num js-line-number" data-line-number="4"></td>
        <td id="LC4" class="blob-code blob-code-inner js-file-line"><span class=pl-k>import</span> <span class=pl-v>ROOT</span></td>
      </tr>
      <tr>
        <td id="L5" class="blob-num js-line-number" data-line-number="5"></td>
        <td id="LC5" class="blob-code blob-code-inner js-file-line"><span class=pl-k>import</span> <span class=pl-s1>math</span></td>
      </tr>
      <tr>
        <td id="L6" class="blob-num js-line-number" data-line-number="6"></td>
        <td id="LC6" class="blob-code blob-code-inner js-file-line"><span class=pl-k>from</span> <span class=pl-s1>variabile</span> <span class=pl-k>import</span> <span class=pl-s1>variabile</span></td>
      </tr>
      <tr>
        <td id="L7" class="blob-num js-line-number" data-line-number="7"></td>
        <td id="LC7" class="blob-code blob-code-inner js-file-line"><span class=pl-k>from</span> <span class=pl-v>CMS_lumi</span> <span class=pl-k>import</span> <span class=pl-v>CMS_lumi</span></td>
      </tr>
      <tr>
        <td id="L8" class="blob-num js-line-number" data-line-number="8"></td>
        <td id="LC8" class="blob-code blob-code-inner js-file-line"><span class=pl-k>from</span> <span class=pl-v>PhysicsTools</span>.<span class=pl-v>NanoAODTools</span>.<span class=pl-s1>postprocessing</span>.<span class=pl-s1>samples</span>.<span class=pl-s1>samples</span> <span class=pl-k>import</span> <span class=pl-c1>*</span></td>
      </tr>
      <tr>
        <td id="L9" class="blob-num js-line-number" data-line-number="9"></td>
        <td id="LC9" class="blob-code blob-code-inner js-file-line"><span class=pl-k>from</span> <span class=pl-s1>array</span> <span class=pl-k>import</span> <span class=pl-s1>array</span></td>
      </tr>
      <tr>
        <td id="L10" class="blob-num js-line-number" data-line-number="10"></td>
        <td id="LC10" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L11" class="blob-num js-line-number" data-line-number="11"></td>
        <td id="LC11" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>usage</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;python makeplot.py&#39;</span></td>
      </tr>
      <tr>
        <td id="L12" class="blob-num js-line-number" data-line-number="12"></td>
        <td id="LC12" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span> <span class=pl-c1>=</span> <span class=pl-s1>optparse</span>.<span class=pl-v>OptionParser</span>(<span class=pl-s1>usage</span>)</td>
      </tr>
      <tr>
        <td id="L13" class="blob-num js-line-number" data-line-number="13"></td>
        <td id="LC13" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;--merpart&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;merpart&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-c1>False</span>, <span class=pl-s1>action</span><span class=pl-c1>=</span><span class=pl-s>&#39;store_true&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default parts are not merged&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L14" class="blob-num js-line-number" data-line-number="14"></td>
        <td id="LC14" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;--mertree&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;mertree&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-c1>False</span>, <span class=pl-s1>action</span><span class=pl-c1>=</span><span class=pl-s>&#39;store_true&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default make no file is merged&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L15" class="blob-num js-line-number" data-line-number="15"></td>
        <td id="LC15" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;--lumi&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;lumi&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-c1>False</span>, <span class=pl-s1>action</span><span class=pl-c1>=</span><span class=pl-s>&#39;store_true&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default do not write the normalization weights&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L16" class="blob-num js-line-number" data-line-number="16"></td>
        <td id="LC16" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;--sel&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;sel&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-c1>False</span>, <span class=pl-s1>action</span><span class=pl-c1>=</span><span class=pl-s>&#39;store_true&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default do not apply any selection&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L17" class="blob-num js-line-number" data-line-number="17"></td>
        <td id="LC17" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-p&#39;</span>, <span class=pl-s>&#39;--plot&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;plot&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-c1>False</span>, <span class=pl-s1>action</span><span class=pl-c1>=</span><span class=pl-s>&#39;store_true&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default make no plots&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L18" class="blob-num js-line-number" data-line-number="18"></td>
        <td id="LC18" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-s&#39;</span>, <span class=pl-s>&#39;--stack&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;stack&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-c1>False</span>, <span class=pl-s1>action</span><span class=pl-c1>=</span><span class=pl-s>&#39;store_true&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default make no stacks&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L19" class="blob-num js-line-number" data-line-number="19"></td>
        <td id="LC19" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-N&#39;</span>, <span class=pl-s>&#39;--notstacked&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;tostack&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-c1>True</span>, <span class=pl-s1>action</span><span class=pl-c1>=</span><span class=pl-s>&#39;store_false&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default make plots stacked&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L20" class="blob-num js-line-number" data-line-number="20"></td>
        <td id="LC20" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-L&#39;</span>, <span class=pl-s>&#39;--lep&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;lep&#39;</span>, <span class=pl-s1>type</span><span class=pl-c1>=</span><span class=pl-s>&#39;string&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;muon&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default make muon analysis&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L21" class="blob-num js-line-number" data-line-number="21"></td>
        <td id="LC21" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-S&#39;</span>, <span class=pl-s>&#39;--syst&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;syst&#39;</span>, <span class=pl-s1>type</span><span class=pl-c1>=</span><span class=pl-s>&#39;string&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;all&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default all systematics added&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L22" class="blob-num js-line-number" data-line-number="22"></td>
        <td id="LC22" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-C&#39;</span>, <span class=pl-s>&#39;--cut&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;cut&#39;</span>, <span class=pl-s1>type</span><span class=pl-c1>=</span><span class=pl-s>&#39;string&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;lepton_eta&gt;-10.&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default no cut&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L23" class="blob-num js-line-number" data-line-number="23"></td>
        <td id="LC23" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-y&#39;</span>, <span class=pl-s>&#39;--year&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;year&#39;</span>, <span class=pl-s1>type</span><span class=pl-c1>=</span><span class=pl-s>&#39;string&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;all&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default 2016, 2017 and 2018 are included&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L24" class="blob-num js-line-number" data-line-number="24"></td>
        <td id="LC24" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-f&#39;</span>, <span class=pl-s>&#39;--folder&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;folder&#39;</span>, <span class=pl-s1>type</span><span class=pl-c1>=</span><span class=pl-s>&#39;string&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;v11&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&#39;Default folder is v0&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L25" class="blob-num js-line-number" data-line-number="25"></td>
        <td id="LC25" class="blob-code blob-code-inner js-file-line"><span class=pl-c>#parser.add_option(&#39;-T&#39;, &#39;--topol&#39;, dest=&#39;topol&#39;, type=&#39;string&#39;, default = &#39;all&#39;, help=&#39;Default all njmt&#39;)</span></td>
      </tr>
      <tr>
        <td id="L26" class="blob-num js-line-number" data-line-number="26"></td>
        <td id="LC26" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>parser</span>.<span class=pl-en>add_option</span>(<span class=pl-s>&#39;-d&#39;</span>, <span class=pl-s>&#39;--dat&#39;</span>, <span class=pl-s1>dest</span><span class=pl-c1>=</span><span class=pl-s>&#39;dat&#39;</span>, <span class=pl-s1>type</span><span class=pl-c1>=</span><span class=pl-s>&#39;string&#39;</span>, <span class=pl-s1>default</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;all&#39;</span>, <span class=pl-s1>help</span><span class=pl-c1>=</span><span class=pl-s>&quot;&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L27" class="blob-num js-line-number" data-line-number="27"></td>
        <td id="LC27" class="blob-code blob-code-inner js-file-line">(<span class=pl-s1>opt</span>, <span class=pl-s1>args</span>) <span class=pl-c1>=</span> <span class=pl-s1>parser</span>.<span class=pl-en>parse_args</span>()</td>
      </tr>
      <tr>
        <td id="L28" class="blob-num js-line-number" data-line-number="28"></td>
        <td id="LC28" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L29" class="blob-num js-line-number" data-line-number="29"></td>
        <td id="LC29" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>folder</span> <span class=pl-c1>=</span> <span class=pl-s1>opt</span>.<span class=pl-s1>folder</span></td>
      </tr>
      <tr>
        <td id="L30" class="blob-num js-line-number" data-line-number="30"></td>
        <td id="LC30" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L31" class="blob-num js-line-number" data-line-number="31"></td>
        <td id="LC31" class="blob-code blob-code-inner js-file-line"><span class=pl-c>#filerepo = &#39;/eos/user/a/apiccine/Wprime/nosynch/v7_apc/&#39;</span></td>
      </tr>
      <tr>
        <td id="L32" class="blob-num js-line-number" data-line-number="32"></td>
        <td id="LC32" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>filerepo</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;/eos/user/&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>os</span>.<span class=pl-s1>environ</span>.<span class=pl-en>get</span>(<span class=pl-s>&#39;USER&#39;</span>)[<span class=pl-c1>0</span>])<span class=pl-c1>+</span><span class=pl-s>&#39;/&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>os</span>.<span class=pl-s1>environ</span>.<span class=pl-en>get</span>(<span class=pl-s>&#39;USER&#39;</span>))<span class=pl-c1>+</span><span class=pl-s>&#39;/Wprime/nosynch/&#39;</span> <span class=pl-c1>+</span> <span class=pl-s1>folder</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;/&#39;</span></td>
      </tr>
      <tr>
        <td id="L33" class="blob-num js-line-number" data-line-number="33"></td>
        <td id="LC33" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>plotrepo</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;/eos/user/&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>os</span>.<span class=pl-s1>environ</span>.<span class=pl-en>get</span>(<span class=pl-s>&#39;USER&#39;</span>)[<span class=pl-c1>0</span>])<span class=pl-c1>+</span><span class=pl-s>&#39;/&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>os</span>.<span class=pl-s1>environ</span>.<span class=pl-en>get</span>(<span class=pl-s>&#39;USER&#39;</span>))<span class=pl-c1>+</span><span class=pl-s>&#39;/Wprime/nosynch/&#39;</span> <span class=pl-c1>+</span> <span class=pl-s1>folder</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;/&#39;</span><span class=pl-c>#_topjet/&#39;#/only_Wpjetbtag_ev1btag/&#39;</span></td>
      </tr>
      <tr>
        <td id="L34" class="blob-num js-line-number" data-line-number="34"></td>
        <td id="LC34" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L35" class="blob-num js-line-number" data-line-number="35"></td>
        <td id="LC35" class="blob-code blob-code-inner js-file-line"><span class=pl-v>ROOT</span>.<span class=pl-s1>gROOT</span>.<span class=pl-v>SetBatch</span>() <span class=pl-c># don&#39;t pop up canvases</span></td>
      </tr>
      <tr>
        <td id="L36" class="blob-num js-line-number" data-line-number="36"></td>
        <td id="LC36" class="blob-code blob-code-inner js-file-line"><span class=pl-k>if</span> <span class=pl-c1>not</span> <span class=pl-s1>os</span>.<span class=pl-s1>path</span>.<span class=pl-en>exists</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;plot/muon&#39;</span>):</td>
      </tr>
      <tr>
        <td id="L37" class="blob-num js-line-number" data-line-number="37"></td>
        <td id="LC37" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>os</span>.<span class=pl-en>makedirs</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;plot/muon&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L38" class="blob-num js-line-number" data-line-number="38"></td>
        <td id="LC38" class="blob-code blob-code-inner js-file-line"><span class=pl-k>if</span> <span class=pl-c1>not</span> <span class=pl-s1>os</span>.<span class=pl-s1>path</span>.<span class=pl-en>exists</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;plot/electron&#39;</span>):</td>
      </tr>
      <tr>
        <td id="L39" class="blob-num js-line-number" data-line-number="39"></td>
        <td id="LC39" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>os</span>.<span class=pl-en>makedirs</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;plot/electron&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L40" class="blob-num js-line-number" data-line-number="40"></td>
        <td id="LC40" class="blob-code blob-code-inner js-file-line"><span class=pl-k>if</span> <span class=pl-c1>not</span> <span class=pl-s1>os</span>.<span class=pl-s1>path</span>.<span class=pl-en>exists</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;stack&#39;</span>):</td>
      </tr>
      <tr>
        <td id="L41" class="blob-num js-line-number" data-line-number="41"></td>
        <td id="LC41" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>os</span>.<span class=pl-en>makedirs</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;stack&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L42" class="blob-num js-line-number" data-line-number="42"></td>
        <td id="LC42" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L43" class="blob-num js-line-number" data-line-number="43"></td>
        <td id="LC43" class="blob-code blob-code-inner js-file-line"><span class=pl-k>def</span> <span class=pl-en>mergepart</span>(<span class=pl-s1>dataset</span>):</td>
      </tr>
      <tr>
        <td id="L44" class="blob-num js-line-number" data-line-number="44"></td>
        <td id="LC44" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>samples</span> <span class=pl-c1>=</span> []</td>
      </tr>
      <tr>
        <td id="L45" class="blob-num js-line-number" data-line-number="45"></td>
        <td id="LC45" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-en>hasattr</span>(<span class=pl-s1>dataset</span>, <span class=pl-s>&#39;components&#39;</span>): <span class=pl-c># How to check whether this exists or not</span></td>
      </tr>
      <tr>
        <td id="L46" class="blob-num js-line-number" data-line-number="46"></td>
        <td id="LC46" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>samples</span> <span class=pl-c1>=</span> [<span class=pl-s1>sample</span> <span class=pl-k>for</span> <span class=pl-s1>sample</span> <span class=pl-c1>in</span> <span class=pl-s1>dataset</span>.<span class=pl-s1>components</span>]<span class=pl-c># Method exists and was used.</span></td>
      </tr>
      <tr>
        <td id="L47" class="blob-num js-line-number" data-line-number="47"></td>
        <td id="LC47" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L48" class="blob-num js-line-number" data-line-number="48"></td>
        <td id="LC48" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>samples</span>.<span class=pl-en>append</span>(<span class=pl-s1>dataset</span>)</td>
      </tr>
      <tr>
        <td id="L49" class="blob-num js-line-number" data-line-number="49"></td>
        <td id="LC49" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>sample</span> <span class=pl-c1>in</span> <span class=pl-s1>samples</span>:</td>
      </tr>
      <tr>
        <td id="L50" class="blob-num js-line-number" data-line-number="50"></td>
        <td id="LC50" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>add</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;hadd -f &quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_merged.root &quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_part*.root&quot;</span> </td>
      </tr>
      <tr>
        <td id="L51" class="blob-num js-line-number" data-line-number="51"></td>
        <td id="LC51" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>print</span> <span class=pl-s1>add</span></td>
      </tr>
      <tr>
        <td id="L52" class="blob-num js-line-number" data-line-number="52"></td>
        <td id="LC52" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>os</span>.<span class=pl-en>system</span>(<span class=pl-en>str</span>(<span class=pl-s1>add</span>))</td>
      </tr>
      <tr>
        <td id="L53" class="blob-num js-line-number" data-line-number="53"></td>
        <td id="LC53" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>check</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TFile</span>.<span class=pl-v>Open</span>(<span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_merged.root &quot;</span>)</td>
      </tr>
      <tr>
        <td id="L54" class="blob-num js-line-number" data-line-number="54"></td>
        <td id="LC54" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>print</span> <span class=pl-s>&quot;Number of entries of the file %s are %s&quot;</span> <span class=pl-c1>%</span>(<span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_merged.root&quot;</span>, (<span class=pl-s1>check</span>.<span class=pl-v>Get</span>(<span class=pl-s>&quot;events_all&quot;</span>)).<span class=pl-v>GetEntries</span>())</td>
      </tr>
      <tr>
        <td id="L55" class="blob-num js-line-number" data-line-number="55"></td>
        <td id="LC55" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L56" class="blob-num js-line-number" data-line-number="56"></td>
        <td id="LC56" class="blob-code blob-code-inner js-file-line"><span class=pl-k>def</span> <span class=pl-en>mergetree</span>(<span class=pl-s1>sample</span>):</td>
      </tr>
      <tr>
        <td id="L57" class="blob-num js-line-number" data-line-number="57"></td>
        <td id="LC57" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-c1>not</span> <span class=pl-s1>os</span>.<span class=pl-s1>path</span>.<span class=pl-en>exists</span>(<span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span>):</td>
      </tr>
      <tr>
        <td id="L58" class="blob-num js-line-number" data-line-number="58"></td>
        <td id="LC58" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>os</span>.<span class=pl-en>makedirs</span>(<span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span>)</td>
      </tr>
      <tr>
        <td id="L59" class="blob-num js-line-number" data-line-number="59"></td>
        <td id="LC59" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>add</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;hadd -f &quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;.root&quot;</span> </td>
      </tr>
      <tr>
        <td id="L60" class="blob-num js-line-number" data-line-number="60"></td>
        <td id="LC60" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>comp</span> <span class=pl-c1>in</span> <span class=pl-s1>sample</span>.<span class=pl-s1>components</span>:</td>
      </tr>
      <tr>
        <td id="L61" class="blob-num js-line-number" data-line-number="61"></td>
        <td id="LC61" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>add</span><span class=pl-c1>+=</span> <span class=pl-s>&quot; &quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>comp</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>comp</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;.root&quot;</span> </td>
      </tr>
      <tr>
        <td id="L62" class="blob-num js-line-number" data-line-number="62"></td>
        <td id="LC62" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>print</span> <span class=pl-s1>add</span></td>
      </tr>
      <tr>
        <td id="L63" class="blob-num js-line-number" data-line-number="63"></td>
        <td id="LC63" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>os</span>.<span class=pl-en>system</span>(<span class=pl-en>str</span>(<span class=pl-s1>add</span>))</td>
      </tr>
      <tr>
        <td id="L64" class="blob-num js-line-number" data-line-number="64"></td>
        <td id="LC64" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L65" class="blob-num js-line-number" data-line-number="65"></td>
        <td id="LC65" class="blob-code blob-code-inner js-file-line"><span class=pl-k>def</span> <span class=pl-en>lumi_writer</span>(<span class=pl-s1>dataset</span>, <span class=pl-s1>lumi</span>):</td>
      </tr>
      <tr>
        <td id="L66" class="blob-num js-line-number" data-line-number="66"></td>
        <td id="LC66" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>samples</span> <span class=pl-c1>=</span> []</td>
      </tr>
      <tr>
        <td id="L67" class="blob-num js-line-number" data-line-number="67"></td>
        <td id="LC67" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-en>hasattr</span>(<span class=pl-s1>dataset</span>, <span class=pl-s>&#39;components&#39;</span>): <span class=pl-c># How to check whether this exists or not</span></td>
      </tr>
      <tr>
        <td id="L68" class="blob-num js-line-number" data-line-number="68"></td>
        <td id="LC68" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>samples</span> <span class=pl-c1>=</span> [<span class=pl-s1>sample</span> <span class=pl-k>for</span> <span class=pl-s1>sample</span> <span class=pl-c1>in</span> <span class=pl-s1>dataset</span>.<span class=pl-s1>components</span>]<span class=pl-c># Method exists and was used.</span></td>
      </tr>
      <tr>
        <td id="L69" class="blob-num js-line-number" data-line-number="69"></td>
        <td id="LC69" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L70" class="blob-num js-line-number" data-line-number="70"></td>
        <td id="LC70" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>samples</span>.<span class=pl-en>append</span>(<span class=pl-s1>dataset</span>)</td>
      </tr>
      <tr>
        <td id="L71" class="blob-num js-line-number" data-line-number="71"></td>
        <td id="LC71" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>sample</span> <span class=pl-c1>in</span> <span class=pl-s1>samples</span>:</td>
      </tr>
      <tr>
        <td id="L72" class="blob-num js-line-number" data-line-number="72"></td>
        <td id="LC72" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span> <span class=pl-c1>not</span> <span class=pl-s>&#39;Data&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span>:</td>
      </tr>
      <tr>
        <td id="L73" class="blob-num js-line-number" data-line-number="73"></td>
        <td id="LC73" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>infile</span> <span class=pl-c1>=</span>  <span class=pl-v>ROOT</span>.<span class=pl-v>TFile</span>.<span class=pl-v>Open</span>(<span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_merged.root&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L74" class="blob-num js-line-number" data-line-number="74"></td>
        <td id="LC74" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tree</span> <span class=pl-c1>=</span> <span class=pl-s1>infile</span>.<span class=pl-v>Get</span>(<span class=pl-s>&#39;events_all&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L75" class="blob-num js-line-number" data-line-number="75"></td>
        <td id="LC75" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tree</span>.<span class=pl-v>SetBranchStatus</span>(<span class=pl-s>&#39;w_nominal&#39;</span>, <span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L76" class="blob-num js-line-number" data-line-number="76"></td>
        <td id="LC76" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tree</span>.<span class=pl-v>SetBranchStatus</span>(<span class=pl-s>&#39;w_PDF&#39;</span>, <span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L77" class="blob-num js-line-number" data-line-number="77"></td>
        <td id="LC77" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>outfile</span> <span class=pl-c1>=</span>  <span class=pl-v>ROOT</span>.<span class=pl-v>TFile</span>.<span class=pl-v>Open</span>(<span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;.root&quot;</span>,<span class=pl-s>&quot;RECREATE&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L78" class="blob-num js-line-number" data-line-number="78"></td>
        <td id="LC78" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tree_new</span> <span class=pl-c1>=</span> <span class=pl-s1>tree</span>.<span class=pl-v>CloneTree</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L79" class="blob-num js-line-number" data-line-number="79"></td>
        <td id="LC79" class="blob-code blob-code-inner js-file-line">               <span class=pl-en>print</span>(<span class=pl-s>&quot;Getting the histos from %s&quot;</span> <span class=pl-c1>%</span>(<span class=pl-s1>infile</span>))</td>
      </tr>
      <tr>
        <td id="L80" class="blob-num js-line-number" data-line-number="80"></td>
        <td id="LC80" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>h_genw_tmp</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>(<span class=pl-s1>infile</span>.<span class=pl-v>Get</span>(<span class=pl-s>&quot;h_genweight&quot;</span>))</td>
      </tr>
      <tr>
        <td id="L81" class="blob-num js-line-number" data-line-number="81"></td>
        <td id="LC81" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>h_pdfw_tmp</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>(<span class=pl-s1>infile</span>.<span class=pl-v>Get</span>(<span class=pl-s>&quot;h_PDFweight&quot;</span>))</td>
      </tr>
      <tr>
        <td id="L82" class="blob-num js-line-number" data-line-number="82"></td>
        <td id="LC82" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>nbins</span> <span class=pl-c1>=</span> <span class=pl-s1>h_pdfw_tmp</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>GetNbins</span>()</td>
      </tr>
      <tr>
        <td id="L83" class="blob-num js-line-number" data-line-number="83"></td>
        <td id="LC83" class="blob-code blob-code-inner js-file-line">               <span class=pl-en>print</span>(<span class=pl-s>&quot;h_genweight first bin content is %f and h_PDFweight has %f bins&quot;</span> <span class=pl-c1>%</span>(<span class=pl-s1>h_genw_tmp</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-c1>1</span>), <span class=pl-s1>nbins</span>))</td>
      </tr>
      <tr>
        <td id="L84" class="blob-num js-line-number" data-line-number="84"></td>
        <td id="LC84" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>w_nom</span> <span class=pl-c1>=</span> <span class=pl-en>array</span>(<span class=pl-s>&#39;f&#39;</span>, [<span class=pl-c1>0.</span>]) </td>
      </tr>
      <tr>
        <td id="L85" class="blob-num js-line-number" data-line-number="85"></td>
        <td id="LC85" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>w_PDF</span> <span class=pl-c1>=</span> <span class=pl-en>array</span>(<span class=pl-s>&#39;f&#39;</span>, [<span class=pl-c1>0.</span>]<span class=pl-c1>*</span><span class=pl-s1>nbins</span>)</td>
      </tr>
      <tr>
        <td id="L86" class="blob-num js-line-number" data-line-number="86"></td>
        <td id="LC86" class="blob-code blob-code-inner js-file-line">               <span class=pl-en>print</span>(<span class=pl-s1>nbins</span>)</td>
      </tr>
      <tr>
        <td id="L87" class="blob-num js-line-number" data-line-number="87"></td>
        <td id="LC87" class="blob-code blob-code-inner js-file-line">               <span class=pl-en>print</span>(<span class=pl-en>len</span>(<span class=pl-s1>w_PDF</span>))</td>
      </tr>
      <tr>
        <td id="L88" class="blob-num js-line-number" data-line-number="88"></td>
        <td id="LC88" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tree_new</span>.<span class=pl-v>Branch</span>(<span class=pl-s>&#39;w_nominal&#39;</span>, <span class=pl-s1>w_nom</span>, <span class=pl-s>&#39;w_nominal/F&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L89" class="blob-num js-line-number" data-line-number="89"></td>
        <td id="LC89" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tree_new</span>.<span class=pl-v>Branch</span>(<span class=pl-s>&#39;w_PDF&#39;</span>, <span class=pl-s1>w_PDF</span>, <span class=pl-s>&#39;w_PDF/F&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L90" class="blob-num js-line-number" data-line-number="90"></td>
        <td id="LC90" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tree</span>.<span class=pl-v>SetBranchStatus</span>(<span class=pl-s>&#39;w_nominal&#39;</span>, <span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L91" class="blob-num js-line-number" data-line-number="91"></td>
        <td id="LC91" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>for</span> <span class=pl-s1>event</span> <span class=pl-c1>in</span> <span class=pl-en>xrange</span>(<span class=pl-c1>0</span>, <span class=pl-s1>tree</span>.<span class=pl-v>GetEntries</span>()):</td>
      </tr>
      <tr>
        <td id="L92" class="blob-num js-line-number" data-line-number="92"></td>
        <td id="LC92" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>tree</span>.<span class=pl-v>GetEntry</span>(<span class=pl-s1>event</span>)</td>
      </tr>
      <tr>
        <td id="L93" class="blob-num js-line-number" data-line-number="93"></td>
        <td id="LC93" class="blob-code blob-code-inner js-file-line">                    <span class=pl-k>if</span> <span class=pl-s1>event</span><span class=pl-c1>%</span><span class=pl-c1>10000</span><span class=pl-c1>==</span><span class=pl-c1>1</span>:</td>
      </tr>
      <tr>
        <td id="L94" class="blob-num js-line-number" data-line-number="94"></td>
        <td id="LC94" class="blob-code blob-code-inner js-file-line">                         <span class=pl-c>#print(&quot;Processing event %s     complete %s percent&quot; %(event, 100*event/tree.GetEntries()))</span></td>
      </tr>
      <tr>
        <td id="L95" class="blob-num js-line-number" data-line-number="95"></td>
        <td id="LC95" class="blob-code blob-code-inner js-file-line">                         <span class=pl-s1>sys</span>.<span class=pl-s1>stdout</span>.<span class=pl-en>write</span>(<span class=pl-s>&quot;<span class=pl-cce>\r</span>Processing event {}     complete {} percent&quot;</span>.<span class=pl-en>format</span>(<span class=pl-s1>event</span>, <span class=pl-c1>100</span><span class=pl-c1>*</span><span class=pl-s1>event</span><span class=pl-c1>/</span><span class=pl-s1>tree</span>.<span class=pl-v>GetEntries</span>()))</td>
      </tr>
      <tr>
        <td id="L96" class="blob-num js-line-number" data-line-number="96"></td>
        <td id="LC96" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>w_nom</span>[<span class=pl-c1>0</span>] <span class=pl-c1>=</span> <span class=pl-s1>tree</span>.<span class=pl-s1>w_nominal</span> <span class=pl-c1>*</span> <span class=pl-s1>sample</span>.<span class=pl-s1>sigma</span> <span class=pl-c1>*</span> <span class=pl-s1>lumi</span> <span class=pl-c1>*</span> <span class=pl-c1>1000.</span><span class=pl-c1>/</span><span class=pl-en>float</span>(<span class=pl-s1>h_genw_tmp</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-c1>1</span>))</td>
      </tr>
      <tr>
        <td id="L97" class="blob-num js-line-number" data-line-number="97"></td>
        <td id="LC97" class="blob-code blob-code-inner js-file-line">                    <span class=pl-k>for</span> <span class=pl-s1>i</span> <span class=pl-c1>in</span> <span class=pl-en>xrange</span>(<span class=pl-c1>1</span>, <span class=pl-s1>nbins</span>):</td>
      </tr>
      <tr>
        <td id="L98" class="blob-num js-line-number" data-line-number="98"></td>
        <td id="LC98" class="blob-code blob-code-inner js-file-line">                         <span class=pl-s1>w_PDF</span>[<span class=pl-s1>i</span>] <span class=pl-c1>=</span> <span class=pl-s1>h_pdfw_tmp</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-s1>i</span><span class=pl-c1>+</span><span class=pl-c1>1</span>)<span class=pl-c1>/</span><span class=pl-s1>h_genw_tmp</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-c1>2</span>) </td>
      </tr>
      <tr>
        <td id="L99" class="blob-num js-line-number" data-line-number="99"></td>
        <td id="LC99" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>tree_new</span>.<span class=pl-v>Fill</span>()</td>
      </tr>
      <tr>
        <td id="L100" class="blob-num js-line-number" data-line-number="100"></td>
        <td id="LC100" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tree_new</span>.<span class=pl-v>Write</span>()</td>
      </tr>
      <tr>
        <td id="L101" class="blob-num js-line-number" data-line-number="101"></td>
        <td id="LC101" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>outfile</span>.<span class=pl-v>Close</span>()</td>
      </tr>
      <tr>
        <td id="L102" class="blob-num js-line-number" data-line-number="102"></td>
        <td id="LC102" class="blob-code blob-code-inner js-file-line">               <span class=pl-en>print</span>(<span class=pl-s>&#39;<span class=pl-cce>\n</span>&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L103" class="blob-num js-line-number" data-line-number="103"></td>
        <td id="LC103" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L104" class="blob-num js-line-number" data-line-number="104"></td>
        <td id="LC104" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>os</span>.<span class=pl-en>popen</span>(<span class=pl-s>&quot;mv &quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_merged.root &quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;.root&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L105" class="blob-num js-line-number" data-line-number="105"></td>
        <td id="LC105" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L106" class="blob-num js-line-number" data-line-number="106"></td>
        <td id="LC106" class="blob-code blob-code-inner js-file-line"><span class=pl-k>def</span> <span class=pl-en>cutToTag</span>(<span class=pl-s1>cut</span>):</td>
      </tr>
      <tr>
        <td id="L107" class="blob-num js-line-number" data-line-number="107"></td>
        <td id="LC107" class="blob-code blob-code-inner js-file-line">    <span class=pl-s1>newstring</span> <span class=pl-c1>=</span> <span class=pl-s1>cut</span>.<span class=pl-en>replace</span>(<span class=pl-s>&quot;-&quot;</span>, <span class=pl-s>&quot;neg&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;&gt;=&quot;</span>,<span class=pl-s>&quot;_GE_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;&gt;&quot;</span>,<span class=pl-s>&quot;_G_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot; &quot;</span>,<span class=pl-s>&quot;&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;&amp;&amp;&quot;</span>,<span class=pl-s>&quot;_AND_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;||&quot;</span>,<span class=pl-s>&quot;_OR_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;&lt;=&quot;</span>,<span class=pl-s>&quot;_LE_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;&lt;&quot;</span>,<span class=pl-s>&quot;_L_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;.&quot;</span>,<span class=pl-s>&quot;p&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;(&quot;</span>,<span class=pl-s>&quot;&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;)&quot;</span>,<span class=pl-s>&quot;&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;==&quot;</span>,<span class=pl-s>&quot;_EQ_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;!=&quot;</span>,<span class=pl-s>&quot;_NEQ_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;=&quot;</span>,<span class=pl-s>&quot;_EQ_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;*&quot;</span>,<span class=pl-s>&quot;_AND_&quot;</span>).<span class=pl-en>replace</span>(<span class=pl-s>&quot;+&quot;</span>,<span class=pl-s>&quot;_OR_&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L108" class="blob-num js-line-number" data-line-number="108"></td>
        <td id="LC108" class="blob-code blob-code-inner js-file-line">    <span class=pl-k>return</span> <span class=pl-s1>newstring</span></td>
      </tr>
      <tr>
        <td id="L109" class="blob-num js-line-number" data-line-number="109"></td>
        <td id="LC109" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L110" class="blob-num js-line-number" data-line-number="110"></td>
        <td id="LC110" class="blob-code blob-code-inner js-file-line"><span class=pl-k>def</span> <span class=pl-en>plot</span>(<span class=pl-s1>lep</span>, <span class=pl-s1>reg</span>, <span class=pl-s1>variable</span>, <span class=pl-s1>sample</span>, <span class=pl-s1>cut_tag</span>, <span class=pl-s1>syst</span>):</td>
      </tr>
      <tr>
        <td id="L111" class="blob-num js-line-number" data-line-number="111"></td>
        <td id="LC111" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>print</span> <span class=pl-s>&quot;plotting &quot;</span>, <span class=pl-s1>variable</span>.<span class=pl-s1>_name</span>, <span class=pl-s>&quot; for sample &quot;</span>, <span class=pl-s1>sample</span>.<span class=pl-s1>label</span>, <span class=pl-s>&quot; with cut &quot;</span>, <span class=pl-s1>cut_tag</span>, <span class=pl-s>&quot; &quot;</span>, <span class=pl-s1>syst</span>,</td>
      </tr>
      <tr>
        <td id="L112" class="blob-num js-line-number" data-line-number="112"></td>
        <td id="LC112" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>ROOT</span>.<span class=pl-v>TH1</span>.<span class=pl-v>SetDefaultSumw2</span>()</td>
      </tr>
      <tr>
        <td id="L113" class="blob-num js-line-number" data-line-number="113"></td>
        <td id="LC113" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>f1</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TFile</span>.<span class=pl-v>Open</span>(<span class=pl-s1>filerepo</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span>  <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;.root&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L114" class="blob-num js-line-number" data-line-number="114"></td>
        <td id="LC114" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>treename</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;events_all&quot;</span></td>
      </tr>
      <tr>
        <td id="L115" class="blob-num js-line-number" data-line-number="115"></td>
        <td id="LC115" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span>(<span class=pl-s1>cut_tag</span> <span class=pl-c1>==</span> <span class=pl-s>&quot;&quot;</span>):</td>
      </tr>
      <tr>
        <td id="L116" class="blob-num js-line-number" data-line-number="116"></td>
        <td id="LC116" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>histoname</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;h_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>reg</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>variable</span>.<span class=pl-s1>_name</span></td>
      </tr>
      <tr>
        <td id="L117" class="blob-num js-line-number" data-line-number="117"></td>
        <td id="LC117" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L118" class="blob-num js-line-number" data-line-number="118"></td>
        <td id="LC118" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>histoname</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;h_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>reg</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>variable</span>.<span class=pl-s1>_name</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>cut_tag</span></td>
      </tr>
      <tr>
        <td id="L119" class="blob-num js-line-number" data-line-number="119"></td>
        <td id="LC119" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>nbins</span> <span class=pl-c1>=</span> <span class=pl-s1>variable</span>.<span class=pl-s1>_nbins</span></td>
      </tr>
      <tr>
        <td id="L120" class="blob-num js-line-number" data-line-number="120"></td>
        <td id="LC120" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h1</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>(<span class=pl-s1>histoname</span>, <span class=pl-s1>variable</span>.<span class=pl-s1>_name</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>reg</span>, <span class=pl-s1>variable</span>.<span class=pl-s1>_nbins</span>, <span class=pl-s1>variable</span>.<span class=pl-s1>_xmin</span>, <span class=pl-s1>variable</span>.<span class=pl-s1>_xmax</span>)</td>
      </tr>
      <tr>
        <td id="L121" class="blob-num js-line-number" data-line-number="121"></td>
        <td id="LC121" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h1</span>.<span class=pl-v>Sumw2</span>()</td>
      </tr>
      <tr>
        <td id="L122" class="blob-num js-line-number" data-line-number="122"></td>
        <td id="LC122" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-s>&#39;muon&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>lep</span>: </td>
      </tr>
      <tr>
        <td id="L123" class="blob-num js-line-number" data-line-number="123"></td>
        <td id="LC123" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>cut</span> <span class=pl-c1>=</span> <span class=pl-s1>variable</span>.<span class=pl-s1>_taglio</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;*isMu*(&#39;</span> <span class=pl-c1>+</span> <span class=pl-en>str</span>(<span class=pl-s1>variable</span>.<span class=pl-s1>_name</span>) <span class=pl-c1>+</span> <span class=pl-s>&quot;&gt;&quot;</span> <span class=pl-c1>+</span> <span class=pl-en>str</span>(<span class=pl-s1>variable</span>.<span class=pl-s1>_xmin</span>) <span class=pl-c1>+</span> <span class=pl-s>&quot;)&quot;</span><span class=pl-c>#&amp;&amp;&quot; + str(variable._name) + &quot;&lt;&quot; + str(variable._xmax) + &quot;)&quot; </span></td>
      </tr>
      <tr>
        <td id="L124" class="blob-num js-line-number" data-line-number="124"></td>
        <td id="LC124" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#if not &#39;Data&#39; in sample.label:</span></td>
      </tr>
      <tr>
        <td id="L125" class="blob-num js-line-number" data-line-number="125"></td>
        <td id="LC125" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#cut += &#39;*passed_mu*(1-passed_ht)&#39;</span></td>
      </tr>
      <tr>
        <td id="L126" class="blob-num js-line-number" data-line-number="126"></td>
        <td id="LC126" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#cut += &#39;*passed_ht*(1-passed_mu)*(1-passed_ele)&#39;</span></td>
      </tr>
      <tr>
        <td id="L127" class="blob-num js-line-number" data-line-number="127"></td>
        <td id="LC127" class="blob-code blob-code-inner js-file-line">          <span class=pl-s>&#39;&#39;&#39;</span></td>
      </tr>
      <tr>
        <td id="L128" class="blob-num js-line-number" data-line-number="128"></td>
        <td id="LC128" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          if &#39;DataMu&#39; in sample.label:</span></td>
      </tr>
      <tr>
        <td id="L129" class="blob-num js-line-number" data-line-number="129"></td>
        <td id="LC129" class="blob-code blob-code-inner js-file-line"><span class=pl-s>               cut += &#39;*passed_ht*(passed_mu)&#39;</span></td>
      </tr>
      <tr>
        <td id="L130" class="blob-num js-line-number" data-line-number="130"></td>
        <td id="LC130" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          elif &#39;DataHT&#39; in sample.label:</span></td>
      </tr>
      <tr>
        <td id="L131" class="blob-num js-line-number" data-line-number="131"></td>
        <td id="LC131" class="blob-code blob-code-inner js-file-line"><span class=pl-s>               cut += &#39;*passed_ht*(1-passed_mu)&#39;</span></td>
      </tr>
      <tr>
        <td id="L132" class="blob-num js-line-number" data-line-number="132"></td>
        <td id="LC132" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          else:</span></td>
      </tr>
      <tr>
        <td id="L133" class="blob-num js-line-number" data-line-number="133"></td>
        <td id="LC133" class="blob-code blob-code-inner js-file-line"><span class=pl-s>               cut += &#39;*passed_ht&#39;</span></td>
      </tr>
      <tr>
        <td id="L134" class="blob-num js-line-number" data-line-number="134"></td>
        <td id="LC134" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          &#39;&#39;&#39;</span></td>
      </tr>
      <tr>
        <td id="L135" class="blob-num js-line-number" data-line-number="135"></td>
        <td id="LC135" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>elif</span> <span class=pl-s>&#39;electron&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>lep</span>:</td>
      </tr>
      <tr>
        <td id="L136" class="blob-num js-line-number" data-line-number="136"></td>
        <td id="LC136" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>cut</span>  <span class=pl-c1>=</span> <span class=pl-s1>variable</span>.<span class=pl-s1>_taglio</span> <span class=pl-c1>+</span> <span class=pl-s>&#39;*isEle*(&#39;</span> <span class=pl-c1>+</span> <span class=pl-en>str</span>(<span class=pl-s1>variable</span>.<span class=pl-s1>_name</span>) <span class=pl-c1>+</span> <span class=pl-s>&quot;&gt;&quot;</span> <span class=pl-c1>+</span> <span class=pl-en>str</span>(<span class=pl-s1>variable</span>.<span class=pl-s1>_xmin</span>) <span class=pl-c1>+</span> <span class=pl-s>&quot;)&quot;</span><span class=pl-c>#&amp;&amp;&quot; + str(variable._name) + &quot;&lt;&quot; + str(variable._xmax) + &quot;)&quot; </span></td>
      </tr>
      <tr>
        <td id="L137" class="blob-num js-line-number" data-line-number="137"></td>
        <td id="LC137" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span> <span class=pl-s>&#39;MC&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>variable</span>.<span class=pl-s1>_name</span>:</td>
      </tr>
      <tr>
        <td id="L138" class="blob-num js-line-number" data-line-number="138"></td>
        <td id="LC138" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>cut</span> <span class=pl-c1>=</span> <span class=pl-s1>cut</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;*(&quot;</span> <span class=pl-c1>+</span> <span class=pl-en>str</span>(<span class=pl-s1>variable</span>.<span class=pl-s1>_name</span>) <span class=pl-c1>+</span> <span class=pl-s>&quot;!=-100.)&quot;</span></td>
      </tr>
      <tr>
        <td id="L139" class="blob-num js-line-number" data-line-number="139"></td>
        <td id="LC139" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#if not &#39;Data&#39; in sample.label: </span></td>
      </tr>
      <tr>
        <td id="L140" class="blob-num js-line-number" data-line-number="140"></td>
        <td id="LC140" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#cut += &#39;*passed_ht*(1-passed_ele)&#39;</span></td>
      </tr>
      <tr>
        <td id="L141" class="blob-num js-line-number" data-line-number="141"></td>
        <td id="LC141" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#cut += &#39;*passed_ele&#39;</span></td>
      </tr>
      <tr>
        <td id="L142" class="blob-num js-line-number" data-line-number="142"></td>
        <td id="LC142" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#if &#39;MC&#39; in variable._name:</span></td>
      </tr>
      <tr>
        <td id="L143" class="blob-num js-line-number" data-line-number="143"></td>
        <td id="LC143" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#if not &#39;Data&#39; in sample.label:</span></td>
      </tr>
      <tr>
        <td id="L144" class="blob-num js-line-number" data-line-number="144"></td>
        <td id="LC144" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#cut = cut + &quot;*(MC_Wprime_m!=-100.)&quot;</span></td>
      </tr>
      <tr>
        <td id="L145" class="blob-num js-line-number" data-line-number="145"></td>
        <td id="LC145" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>print</span> <span class=pl-en>str</span>(<span class=pl-s1>cut</span>)</td>
      </tr>
      <tr>
        <td id="L146" class="blob-num js-line-number" data-line-number="146"></td>
        <td id="LC146" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>foutput</span> <span class=pl-c1>=</span> <span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;plot/&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>lep</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>lep</span><span class=pl-c1>+</span><span class=pl-s>&quot;.root&quot;</span></td>
      </tr>
      <tr>
        <td id="L147" class="blob-num js-line-number" data-line-number="147"></td>
        <td id="LC147" class="blob-code blob-code-inner js-file-line">     <span class=pl-s>&#39;&#39;&#39;</span></td>
      </tr>
      <tr>
        <td id="L148" class="blob-num js-line-number" data-line-number="148"></td>
        <td id="LC148" class="blob-code blob-code-inner js-file-line"><span class=pl-s>     else:</span></td>
      </tr>
      <tr>
        <td id="L149" class="blob-num js-line-number" data-line-number="149"></td>
        <td id="LC149" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          if(syst==&quot;&quot;):</span></td>
      </tr>
      <tr>
        <td id="L150" class="blob-num js-line-number" data-line-number="150"></td>
        <td id="LC150" class="blob-code blob-code-inner js-file-line"><span class=pl-s>            taglio = variable._taglio+&quot;*w_nominal&quot;</span></td>
      </tr>
      <tr>
        <td id="L151" class="blob-num js-line-number" data-line-number="151"></td>
        <td id="LC151" class="blob-code blob-code-inner js-file-line"><span class=pl-s>            foutput = &quot;Plot/&quot;+lep+&quot;/&quot;+channel+&quot;_&quot;+lep+&quot;.root&quot;</span></td>
      </tr>
      <tr>
        <td id="L152" class="blob-num js-line-number" data-line-number="152"></td>
        <td id="LC152" class="blob-code blob-code-inner js-file-line"><span class=pl-s>        elif(syst.startswith(&quot;jer&quot;) or syst.startswith(&quot;jes&quot;)):</span></td>
      </tr>
      <tr>
        <td id="L153" class="blob-num js-line-number" data-line-number="153"></td>
        <td id="LC153" class="blob-code blob-code-inner js-file-line"><span class=pl-s>            taglio = variable._taglio+&quot;*w_nominal&quot;</span></td>
      </tr>
      <tr>
        <td id="L154" class="blob-num js-line-number" data-line-number="154"></td>
        <td id="LC154" class="blob-code blob-code-inner js-file-line"><span class=pl-s>            treename = &quot;events_&quot;+reg+&quot;_&quot;+syst</span></td>
      </tr>
      <tr>
        <td id="L155" class="blob-num js-line-number" data-line-number="155"></td>
        <td id="LC155" class="blob-code blob-code-inner js-file-line"><span class=pl-s>            foutput = &quot;Plot/&quot;+lep+&quot;/&quot;+channel+&quot;_&quot;+lep+&quot;_&quot;+syst+&quot;.root&quot;</span></td>
      </tr>
      <tr>
        <td id="L156" class="blob-num js-line-number" data-line-number="156"></td>
        <td id="LC156" class="blob-code blob-code-inner js-file-line"><span class=pl-s>            if(channel == &quot;WJets_ext&quot; and lep.startswith(&quot;electron&quot;)):</span></td>
      </tr>
      <tr>
        <td id="L157" class="blob-num js-line-number" data-line-number="157"></td>
        <td id="LC157" class="blob-code blob-code-inner js-file-line"><span class=pl-s>                taglio = variable._taglio+&quot;*w_nominal*(abs(w)&lt;10)&quot;</span></td>
      </tr>
      <tr>
        <td id="L158" class="blob-num js-line-number" data-line-number="158"></td>
        <td id="LC158" class="blob-code blob-code-inner js-file-line"><span class=pl-s>     &#39;&#39;&#39;</span></td>
      </tr>
      <tr>
        <td id="L159" class="blob-num js-line-number" data-line-number="159"></td>
        <td id="LC159" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#print treename</span></td>
      </tr>
      <tr>
        <td id="L160" class="blob-num js-line-number" data-line-number="160"></td>
        <td id="LC160" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>f1</span>.<span class=pl-v>Get</span>(<span class=pl-s1>treename</span>).<span class=pl-v>Project</span>(<span class=pl-s1>histoname</span>,<span class=pl-s1>variable</span>.<span class=pl-s1>_name</span>,<span class=pl-s1>cut</span>)</td>
      </tr>
      <tr>
        <td id="L161" class="blob-num js-line-number" data-line-number="161"></td>
        <td id="LC161" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#if not &#39;Data&#39; in sample.label:</span></td>
      </tr>
      <tr>
        <td id="L162" class="blob-num js-line-number" data-line-number="162"></td>
        <td id="LC162" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#     h1.Scale((7.5)/35.89)</span></td>
      </tr>
      <tr>
        <td id="L163" class="blob-num js-line-number" data-line-number="163"></td>
        <td id="LC163" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h1</span>.<span class=pl-v>SetBinContent</span>(<span class=pl-c1>1</span>, <span class=pl-s1>h1</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-c1>0</span>) <span class=pl-c1>+</span> <span class=pl-s1>h1</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-c1>1</span>))</td>
      </tr>
      <tr>
        <td id="L164" class="blob-num js-line-number" data-line-number="164"></td>
        <td id="LC164" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h1</span>.<span class=pl-v>SetBinError</span>(<span class=pl-c1>1</span>, <span class=pl-s1>math</span>.<span class=pl-en>sqrt</span>(<span class=pl-en>pow</span>(<span class=pl-s1>h1</span>.<span class=pl-v>GetBinError</span>(<span class=pl-c1>0</span>),<span class=pl-c1>2</span>) <span class=pl-c1>+</span> <span class=pl-en>pow</span>(<span class=pl-s1>h1</span>.<span class=pl-v>GetBinError</span>(<span class=pl-c1>1</span>),<span class=pl-c1>2</span>)))</td>
      </tr>
      <tr>
        <td id="L165" class="blob-num js-line-number" data-line-number="165"></td>
        <td id="LC165" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h1</span>.<span class=pl-v>SetBinContent</span>(<span class=pl-s1>nbins</span>, <span class=pl-s1>h1</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-s1>nbins</span>) <span class=pl-c1>+</span> <span class=pl-s1>h1</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-s1>nbins</span><span class=pl-c1>+</span><span class=pl-c1>1</span>))</td>
      </tr>
      <tr>
        <td id="L166" class="blob-num js-line-number" data-line-number="166"></td>
        <td id="LC166" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h1</span>.<span class=pl-v>SetBinError</span>(<span class=pl-s1>nbins</span>, <span class=pl-s1>math</span>.<span class=pl-en>sqrt</span>(<span class=pl-en>pow</span>(<span class=pl-s1>h1</span>.<span class=pl-v>GetBinError</span>(<span class=pl-s1>nbins</span>),<span class=pl-c1>2</span>) <span class=pl-c1>+</span> <span class=pl-en>pow</span>(<span class=pl-s1>h1</span>.<span class=pl-v>GetBinError</span>(<span class=pl-s1>nbins</span><span class=pl-c1>+</span><span class=pl-c1>1</span>),<span class=pl-c1>2</span>)))</td>
      </tr>
      <tr>
        <td id="L167" class="blob-num js-line-number" data-line-number="167"></td>
        <td id="LC167" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>i</span> <span class=pl-c1>in</span> <span class=pl-en>range</span>(<span class=pl-c1>0</span>, <span class=pl-s1>nbins</span><span class=pl-c1>+</span><span class=pl-c1>1</span>):</td>
      </tr>
      <tr>
        <td id="L168" class="blob-num js-line-number" data-line-number="168"></td>
        <td id="LC168" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>content</span> <span class=pl-c1>=</span> <span class=pl-s1>h1</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-s1>i</span>)</td>
      </tr>
      <tr>
        <td id="L169" class="blob-num js-line-number" data-line-number="169"></td>
        <td id="LC169" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s1>content</span><span class=pl-c1>&lt;</span><span class=pl-c1>0.</span>):</td>
      </tr>
      <tr>
        <td id="L170" class="blob-num js-line-number" data-line-number="170"></td>
        <td id="LC170" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>h1</span>.<span class=pl-v>SetBinContent</span>(<span class=pl-s1>i</span>, <span class=pl-c1>0.</span>)</td>
      </tr>
      <tr>
        <td id="L171" class="blob-num js-line-number" data-line-number="171"></td>
        <td id="LC171" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>fout</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TFile</span>.<span class=pl-v>Open</span>(<span class=pl-s1>foutput</span>, <span class=pl-s>&quot;UPDATE&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L172" class="blob-num js-line-number" data-line-number="172"></td>
        <td id="LC172" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>fout</span>.<span class=pl-en>cd</span>()</td>
      </tr>
      <tr>
        <td id="L173" class="blob-num js-line-number" data-line-number="173"></td>
        <td id="LC173" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h1</span>.<span class=pl-v>Write</span>()</td>
      </tr>
      <tr>
        <td id="L174" class="blob-num js-line-number" data-line-number="174"></td>
        <td id="LC174" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>fout</span>.<span class=pl-v>Close</span>()</td>
      </tr>
      <tr>
        <td id="L175" class="blob-num js-line-number" data-line-number="175"></td>
        <td id="LC175" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>f1</span>.<span class=pl-v>Close</span>()</td>
      </tr>
      <tr>
        <td id="L176" class="blob-num js-line-number" data-line-number="176"></td>
        <td id="LC176" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L177" class="blob-num js-line-number" data-line-number="177"></td>
        <td id="LC177" class="blob-code blob-code-inner js-file-line"><span class=pl-k>def</span> <span class=pl-en>makestack</span>(<span class=pl-s1>lep_</span>, <span class=pl-s1>reg_</span>, <span class=pl-s1>variabile_</span>, <span class=pl-s1>samples_</span>, <span class=pl-s1>cut_tag_</span>, <span class=pl-s1>syst_</span>, <span class=pl-s1>lumi</span>):</td>
      </tr>
      <tr>
        <td id="L178" class="blob-num js-line-number" data-line-number="178"></td>
        <td id="LC178" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>os</span>.<span class=pl-en>system</span>(<span class=pl-s>&#39;set LD_PRELOAD=libtcmalloc.so&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L179" class="blob-num js-line-number" data-line-number="179"></td>
        <td id="LC179" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>blind</span> <span class=pl-c1>=</span> <span class=pl-c1>False</span></td>
      </tr>
      <tr>
        <td id="L180" class="blob-num js-line-number" data-line-number="180"></td>
        <td id="LC180" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>infile</span> <span class=pl-c1>=</span> {}</td>
      </tr>
      <tr>
        <td id="L181" class="blob-num js-line-number" data-line-number="181"></td>
        <td id="LC181" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>histo</span> <span class=pl-c1>=</span> []</td>
      </tr>
      <tr>
        <td id="L182" class="blob-num js-line-number" data-line-number="182"></td>
        <td id="LC182" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>tmp</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>()</td>
      </tr>
      <tr>
        <td id="L183" class="blob-num js-line-number" data-line-number="183"></td>
        <td id="LC183" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>()</td>
      </tr>
      <tr>
        <td id="L184" class="blob-num js-line-number" data-line-number="184"></td>
        <td id="LC184" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>hdata</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>(<span class=pl-s>&#39;h&#39;</span>,<span class=pl-s>&#39;h&#39;</span>, <span class=pl-s1>variabile_</span>.<span class=pl-s1>_nbins</span>, <span class=pl-s1>variabile_</span>.<span class=pl-s1>_xmin</span>, <span class=pl-s1>variabile_</span>.<span class=pl-s1>_xmax</span>)</td>
      </tr>
      <tr>
        <td id="L185" class="blob-num js-line-number" data-line-number="185"></td>
        <td id="LC185" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_sig</span> <span class=pl-c1>=</span> []</td>
      </tr>
      <tr>
        <td id="L186" class="blob-num js-line-number" data-line-number="186"></td>
        <td id="LC186" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_err</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>()</td>
      </tr>
      <tr>
        <td id="L187" class="blob-num js-line-number" data-line-number="187"></td>
        <td id="LC187" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>()</td>
      </tr>
      <tr>
        <td id="L188" class="blob-num js-line-number" data-line-number="188"></td>
        <td id="LC188" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>print</span> <span class=pl-s>&quot;Variabile:&quot;</span>, <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span></td>
      </tr>
      <tr>
        <td id="L189" class="blob-num js-line-number" data-line-number="189"></td>
        <td id="LC189" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>ROOT</span>.<span class=pl-s1>gROOT</span>.<span class=pl-v>SetStyle</span>(<span class=pl-s>&#39;Plain&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L190" class="blob-num js-line-number" data-line-number="190"></td>
        <td id="LC190" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>ROOT</span>.<span class=pl-s1>gStyle</span>.<span class=pl-v>SetPalette</span>(<span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L191" class="blob-num js-line-number" data-line-number="191"></td>
        <td id="LC191" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>ROOT</span>.<span class=pl-s1>gStyle</span>.<span class=pl-v>SetOptStat</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L192" class="blob-num js-line-number" data-line-number="192"></td>
        <td id="LC192" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>ROOT</span>.<span class=pl-v>TH1</span>.<span class=pl-v>SetDefaultSumw2</span>()</td>
      </tr>
      <tr>
        <td id="L193" class="blob-num js-line-number" data-line-number="193"></td>
        <td id="LC193" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span>(<span class=pl-s1>cut_tag_</span> <span class=pl-c1>==</span> <span class=pl-s>&quot;&quot;</span>):</td>
      </tr>
      <tr>
        <td id="L194" class="blob-num js-line-number" data-line-number="194"></td>
        <td id="LC194" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>histoname</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;h_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>reg_</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span></td>
      </tr>
      <tr>
        <td id="L195" class="blob-num js-line-number" data-line-number="195"></td>
        <td id="LC195" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>stackname</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;stack_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>reg_</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span></td>
      </tr>
      <tr>
        <td id="L196" class="blob-num js-line-number" data-line-number="196"></td>
        <td id="LC196" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>canvasname</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;stack_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>reg_</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>lep_</span></td>
      </tr>
      <tr>
        <td id="L197" class="blob-num js-line-number" data-line-number="197"></td>
        <td id="LC197" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L198" class="blob-num js-line-number" data-line-number="198"></td>
        <td id="LC198" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>histoname</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;h_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>reg_</span><span class=pl-c1>+</span><span class=pl-s>&quot;_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span><span class=pl-c1>+</span><span class=pl-s>&quot;_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>cut_tag_</span></td>
      </tr>
      <tr>
        <td id="L199" class="blob-num js-line-number" data-line-number="199"></td>
        <td id="LC199" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>stackname</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;stack_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>reg_</span><span class=pl-c1>+</span><span class=pl-s>&quot;_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span><span class=pl-c1>+</span><span class=pl-s>&quot;_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>cut_tag_</span></td>
      </tr>
      <tr>
        <td id="L200" class="blob-num js-line-number" data-line-number="200"></td>
        <td id="LC200" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>canvasname</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;stack_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>reg_</span><span class=pl-c1>+</span><span class=pl-s>&quot;_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span><span class=pl-c1>+</span><span class=pl-s>&quot;_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>cut_tag_</span><span class=pl-c1>+</span><span class=pl-s>&quot;_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>lep_</span></td>
      </tr>
      <tr>
        <td id="L201" class="blob-num js-line-number" data-line-number="201"></td>
        <td id="LC201" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span>(<span class=pl-s>&quot;selection_AND_best_Wpjet_isbtag_AND_best_topjet_isbtag&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>cut_tag_</span> ) <span class=pl-c1>or</span> (<span class=pl-s>&quot;selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>cut_tag_</span> ):</td>
      </tr>
      <tr>
        <td id="L202" class="blob-num js-line-number" data-line-number="202"></td>
        <td id="LC202" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>blind</span> <span class=pl-c1>=</span> <span class=pl-c1>True</span></td>
      </tr>
      <tr>
        <td id="L203" class="blob-num js-line-number" data-line-number="203"></td>
        <td id="LC203" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>THStack</span>(<span class=pl-s1>stackname</span>, <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span>)</td>
      </tr>
      <tr>
        <td id="L204" class="blob-num js-line-number" data-line-number="204"></td>
        <td id="LC204" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TLegend</span>(<span class=pl-c1>0.33</span>,<span class=pl-c1>0.62</span>,<span class=pl-c1>0.91</span>,<span class=pl-c1>0.87</span>)</td>
      </tr>
      <tr>
        <td id="L205" class="blob-num js-line-number" data-line-number="205"></td>
        <td id="LC205" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>signal</span> <span class=pl-c1>=</span> <span class=pl-c1>False</span></td>
      </tr>
      <tr>
        <td id="L206" class="blob-num js-line-number" data-line-number="206"></td>
        <td id="LC206" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L207" class="blob-num js-line-number" data-line-number="207"></td>
        <td id="LC207" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>print</span> <span class=pl-s1>samples_</span></td>
      </tr>
      <tr>
        <td id="L208" class="blob-num js-line-number" data-line-number="208"></td>
        <td id="LC208" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>s</span> <span class=pl-c1>in</span> <span class=pl-s1>samples_</span>:</td>
      </tr>
      <tr>
        <td id="L209" class="blob-num js-line-number" data-line-number="209"></td>
        <td id="LC209" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s>&#39;WP&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>s</span>.<span class=pl-s1>label</span>):</td>
      </tr>
      <tr>
        <td id="L210" class="blob-num js-line-number" data-line-number="210"></td>
        <td id="LC210" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>signal</span> <span class=pl-c1>=</span> <span class=pl-c1>True</span></td>
      </tr>
      <tr>
        <td id="L211" class="blob-num js-line-number" data-line-number="211"></td>
        <td id="LC211" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s1>syst_</span> <span class=pl-c1>==</span> <span class=pl-s>&quot;&quot;</span>):</td>
      </tr>
      <tr>
        <td id="L212" class="blob-num js-line-number" data-line-number="212"></td>
        <td id="LC212" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>outfile</span> <span class=pl-c1>=</span> <span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;stack_&quot;</span> <span class=pl-c1>+</span> <span class=pl-en>str</span>(<span class=pl-s1>lep_</span>).<span class=pl-en>strip</span>(<span class=pl-s>&#39;[]&#39;</span>) <span class=pl-c1>+</span> <span class=pl-s>&quot;.root&quot;</span></td>
      </tr>
      <tr>
        <td id="L213" class="blob-num js-line-number" data-line-number="213"></td>
        <td id="LC213" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>infile</span>[<span class=pl-s1>s</span>.<span class=pl-s1>label</span>] <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TFile</span>.<span class=pl-v>Open</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;plot/&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>lep</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>s</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>lep</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;.root&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L214" class="blob-num js-line-number" data-line-number="214"></td>
        <td id="LC214" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L215" class="blob-num js-line-number" data-line-number="215"></td>
        <td id="LC215" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>outfile</span> <span class=pl-c1>=</span> <span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;stack_&quot;</span><span class=pl-c1>+</span><span class=pl-s1>syst_</span><span class=pl-c1>+</span><span class=pl-s>&quot;_&quot;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>lep_</span>).<span class=pl-en>strip</span>(<span class=pl-s>&#39;[]&#39;</span>)<span class=pl-c1>+</span><span class=pl-s>&quot;.root&quot;</span></td>
      </tr>
      <tr>
        <td id="L216" class="blob-num js-line-number" data-line-number="216"></td>
        <td id="LC216" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>infile</span>[<span class=pl-s1>s</span>.<span class=pl-s1>label</span>] <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TFile</span>.<span class=pl-v>Open</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;plot/&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>lep</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;/&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>s</span>.<span class=pl-s1>label</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>lep</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;_&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>syst_</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;.root&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L217" class="blob-num js-line-number" data-line-number="217"></td>
        <td id="LC217" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>i</span> <span class=pl-c1>=</span> <span class=pl-c1>0</span></td>
      </tr>
      <tr>
        <td id="L218" class="blob-num js-line-number" data-line-number="218"></td>
        <td id="LC218" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L219" class="blob-num js-line-number" data-line-number="219"></td>
        <td id="LC219" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>s</span> <span class=pl-c1>in</span> <span class=pl-s1>samples_</span>:</td>
      </tr>
      <tr>
        <td id="L220" class="blob-num js-line-number" data-line-number="220"></td>
        <td id="LC220" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>infile</span>[<span class=pl-s1>s</span>.<span class=pl-s1>label</span>].<span class=pl-en>cd</span>()</td>
      </tr>
      <tr>
        <td id="L221" class="blob-num js-line-number" data-line-number="221"></td>
        <td id="LC221" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>print</span> <span class=pl-s>&quot;opening file: &quot;</span>, <span class=pl-s1>infile</span>[<span class=pl-s1>s</span>.<span class=pl-s1>label</span>].<span class=pl-v>GetName</span>()</td>
      </tr>
      <tr>
        <td id="L222" class="blob-num js-line-number" data-line-number="222"></td>
        <td id="LC222" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s>&#39;Data&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>s</span>.<span class=pl-s1>label</span>):</td>
      </tr>
      <tr>
        <td id="L223" class="blob-num js-line-number" data-line-number="223"></td>
        <td id="LC223" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>if</span> (<span class=pl-s>&quot;GenPart&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span>) <span class=pl-c1>or</span> (<span class=pl-s>&quot;MC_&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span>):</td>
      </tr>
      <tr>
        <td id="L224" class="blob-num js-line-number" data-line-number="224"></td>
        <td id="LC224" class="blob-code blob-code-inner js-file-line">                    <span class=pl-k>continue</span></td>
      </tr>
      <tr>
        <td id="L225" class="blob-num js-line-number" data-line-number="225"></td>
        <td id="LC225" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>tmp</span> <span class=pl-c1>=</span> (<span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>)(<span class=pl-s1>infile</span>[<span class=pl-s1>s</span>.<span class=pl-s1>label</span>].<span class=pl-v>Get</span>(<span class=pl-s1>histoname</span>))</td>
      </tr>
      <tr>
        <td id="L226" class="blob-num js-line-number" data-line-number="226"></td>
        <td id="LC226" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>tmp</span>.<span class=pl-v>SetLineColor</span>(<span class=pl-v>ROOT</span>.<span class=pl-s1>kBlack</span>)</td>
      </tr>
      <tr>
        <td id="L227" class="blob-num js-line-number" data-line-number="227"></td>
        <td id="LC227" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>tmp</span>.<span class=pl-v>SetName</span>(<span class=pl-s1>s</span>.<span class=pl-s1>leglabel</span>)</td>
      </tr>
      <tr>
        <td id="L228" class="blob-num js-line-number" data-line-number="228"></td>
        <td id="LC228" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>print</span> <span class=pl-s1>s</span>.<span class=pl-s1>label</span> </td>
      </tr>
      <tr>
        <td id="L229" class="blob-num js-line-number" data-line-number="229"></td>
        <td id="LC229" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>print</span> <span class=pl-s1>blind</span></td>
      </tr>
      <tr>
        <td id="L230" class="blob-num js-line-number" data-line-number="230"></td>
        <td id="LC230" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s>&#39;Data&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>s</span>.<span class=pl-s1>label</span>):</td>
      </tr>
      <tr>
        <td id="L231" class="blob-num js-line-number" data-line-number="231"></td>
        <td id="LC231" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>if</span> (<span class=pl-s>&quot;GenPart&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span>) <span class=pl-c1>or</span> (<span class=pl-s>&quot;MC_&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_name</span>):</td>
      </tr>
      <tr>
        <td id="L232" class="blob-num js-line-number" data-line-number="232"></td>
        <td id="LC232" class="blob-code blob-code-inner js-file-line">                    <span class=pl-k>continue</span></td>
      </tr>
      <tr>
        <td id="L233" class="blob-num js-line-number" data-line-number="233"></td>
        <td id="LC233" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>hdata</span>.<span class=pl-v>Add</span>(<span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>(<span class=pl-s1>tmp</span>.<span class=pl-v>Clone</span>(<span class=pl-s>&quot;&quot;</span>)))</td>
      </tr>
      <tr>
        <td id="L234" class="blob-num js-line-number" data-line-number="234"></td>
        <td id="LC234" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>hdata</span>.<span class=pl-v>SetMarkerStyle</span>(<span class=pl-c1>20</span>)</td>
      </tr>
      <tr>
        <td id="L235" class="blob-num js-line-number" data-line-number="235"></td>
        <td id="LC235" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>hdata</span>.<span class=pl-v>SetMarkerSize</span>(<span class=pl-c1>0.9</span>)</td>
      </tr>
      <tr>
        <td id="L236" class="blob-num js-line-number" data-line-number="236"></td>
        <td id="LC236" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>if</span>(<span class=pl-s1>i</span> <span class=pl-c1>==</span> <span class=pl-c1>0</span> <span class=pl-c1>and</span> <span class=pl-c1>not</span> <span class=pl-s1>blind</span>): <span class=pl-c># trick to add Data flag to legend only once</span></td>
      </tr>
      <tr>
        <td id="L237" class="blob-num js-line-number" data-line-number="237"></td>
        <td id="LC237" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>leg_stack</span>.<span class=pl-v>AddEntry</span>(<span class=pl-s1>hdata</span>, <span class=pl-s>&quot;Data&quot;</span>, <span class=pl-s>&quot;ep&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L238" class="blob-num js-line-number" data-line-number="238"></td>
        <td id="LC238" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>i</span> <span class=pl-c1>+=</span> <span class=pl-c1>1</span></td>
      </tr>
      <tr>
        <td id="L239" class="blob-num js-line-number" data-line-number="239"></td>
        <td id="LC239" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>elif</span>(<span class=pl-s>&#39;WP&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>s</span>.<span class=pl-s1>label</span>):</td>
      </tr>
      <tr>
        <td id="L240" class="blob-num js-line-number" data-line-number="240"></td>
        <td id="LC240" class="blob-code blob-code-inner js-file-line">               <span class=pl-c>#tmp.SetLineStyle(9)</span></td>
      </tr>
      <tr>
        <td id="L241" class="blob-num js-line-number" data-line-number="241"></td>
        <td id="LC241" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>if</span> <span class=pl-s1>opt</span>.<span class=pl-s1>tostack</span>:</td>
      </tr>
      <tr>
        <td id="L242" class="blob-num js-line-number" data-line-number="242"></td>
        <td id="LC242" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>tmp</span>.<span class=pl-v>SetFillColor</span>(<span class=pl-s1>s</span>.<span class=pl-s1>color</span>)</td>
      </tr>
      <tr>
        <td id="L243" class="blob-num js-line-number" data-line-number="243"></td>
        <td id="LC243" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L244" class="blob-num js-line-number" data-line-number="244"></td>
        <td id="LC244" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>tmp</span>.<span class=pl-v>SetLineColor</span>(<span class=pl-s1>s</span>.<span class=pl-s1>color</span>)</td>
      </tr>
      <tr>
        <td id="L245" class="blob-num js-line-number" data-line-number="245"></td>
        <td id="LC245" class="blob-code blob-code-inner js-file-line">               <span class=pl-c>#tmp.SetLineWidth(3)</span></td>
      </tr>
      <tr>
        <td id="L246" class="blob-num js-line-number" data-line-number="246"></td>
        <td id="LC246" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tmp</span>.<span class=pl-v>SetMarkerSize</span>(<span class=pl-c1>0.</span>)</td>
      </tr>
      <tr>
        <td id="L247" class="blob-num js-line-number" data-line-number="247"></td>
        <td id="LC247" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tmp</span>.<span class=pl-v>SetMarkerColor</span>(<span class=pl-s1>s</span>.<span class=pl-s1>color</span>)</td>
      </tr>
      <tr>
        <td id="L248" class="blob-num js-line-number" data-line-number="248"></td>
        <td id="LC248" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>h_sig</span>.<span class=pl-en>append</span>(<span class=pl-v>ROOT</span>.<span class=pl-v>TH1F</span>(<span class=pl-s1>tmp</span>.<span class=pl-v>Clone</span>(<span class=pl-s>&quot;&quot;</span>)))</td>
      </tr>
      <tr>
        <td id="L249" class="blob-num js-line-number" data-line-number="249"></td>
        <td id="LC249" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L250" class="blob-num js-line-number" data-line-number="250"></td>
        <td id="LC250" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tmp</span>.<span class=pl-v>SetOption</span>(<span class=pl-s>&quot;HIST SAME&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L251" class="blob-num js-line-number" data-line-number="251"></td>
        <td id="LC251" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>tmp</span>.<span class=pl-v>SetTitle</span>(<span class=pl-s>&quot;&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L252" class="blob-num js-line-number" data-line-number="252"></td>
        <td id="LC252" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>if</span> <span class=pl-s1>opt</span>.<span class=pl-s1>tostack</span>:</td>
      </tr>
      <tr>
        <td id="L253" class="blob-num js-line-number" data-line-number="253"></td>
        <td id="LC253" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>tmp</span>.<span class=pl-v>SetFillColor</span>(<span class=pl-s1>s</span>.<span class=pl-s1>color</span>)</td>
      </tr>
      <tr>
        <td id="L254" class="blob-num js-line-number" data-line-number="254"></td>
        <td id="LC254" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L255" class="blob-num js-line-number" data-line-number="255"></td>
        <td id="LC255" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>tmp</span>.<span class=pl-v>SetLineColor</span>(<span class=pl-s1>s</span>.<span class=pl-s1>color</span>)</td>
      </tr>
      <tr>
        <td id="L256" class="blob-num js-line-number" data-line-number="256"></td>
        <td id="LC256" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>histo</span>.<span class=pl-en>append</span>(<span class=pl-s1>tmp</span>.<span class=pl-v>Clone</span>(<span class=pl-s>&quot;&quot;</span>))</td>
      </tr>
      <tr>
        <td id="L257" class="blob-num js-line-number" data-line-number="257"></td>
        <td id="LC257" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>stack</span>.<span class=pl-v>Add</span>(<span class=pl-s1>tmp</span>.<span class=pl-v>Clone</span>(<span class=pl-s>&quot;&quot;</span>))</td>
      </tr>
      <tr>
        <td id="L258" class="blob-num js-line-number" data-line-number="258"></td>
        <td id="LC258" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>tmp</span>.<span class=pl-v>Reset</span>(<span class=pl-s>&quot;ICES&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L259" class="blob-num js-line-number" data-line-number="259"></td>
        <td id="LC259" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>hist</span> <span class=pl-c1>in</span> <span class=pl-en>reversed</span>(<span class=pl-s1>histo</span>):</td>
      </tr>
      <tr>
        <td id="L260" class="blob-num js-line-number" data-line-number="260"></td>
        <td id="LC260" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span> <span class=pl-c1>not</span> (<span class=pl-s>&#39;Data&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>hist</span>.<span class=pl-v>GetName</span>()):</td>
      </tr>
      <tr>
        <td id="L261" class="blob-num js-line-number" data-line-number="261"></td>
        <td id="LC261" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>leg_stack</span>.<span class=pl-v>AddEntry</span>(<span class=pl-s1>hist</span>, <span class=pl-s1>hist</span>.<span class=pl-v>GetName</span>(), <span class=pl-s>&quot;f&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L262" class="blob-num js-line-number" data-line-number="262"></td>
        <td id="LC262" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#style options</span></td>
      </tr>
      <tr>
        <td id="L263" class="blob-num js-line-number" data-line-number="263"></td>
        <td id="LC263" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span>.<span class=pl-v>SetNColumns</span>(<span class=pl-c1>2</span>)</td>
      </tr>
      <tr>
        <td id="L264" class="blob-num js-line-number" data-line-number="264"></td>
        <td id="LC264" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span>.<span class=pl-v>SetFillColor</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L265" class="blob-num js-line-number" data-line-number="265"></td>
        <td id="LC265" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span>.<span class=pl-v>SetFillStyle</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L266" class="blob-num js-line-number" data-line-number="266"></td>
        <td id="LC266" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span>.<span class=pl-v>SetTextFont</span>(<span class=pl-c1>42</span>)</td>
      </tr>
      <tr>
        <td id="L267" class="blob-num js-line-number" data-line-number="267"></td>
        <td id="LC267" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span>.<span class=pl-v>SetBorderSize</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L268" class="blob-num js-line-number" data-line-number="268"></td>
        <td id="LC268" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span>.<span class=pl-v>SetTextSize</span>(<span class=pl-c1>0.05</span>)</td>
      </tr>
      <tr>
        <td id="L269" class="blob-num js-line-number" data-line-number="269"></td>
        <td id="LC269" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TCanvas</span>(<span class=pl-s1>canvasname</span>,<span class=pl-s>&quot;c1&quot;</span>,<span class=pl-c1>50</span>,<span class=pl-c1>50</span>,<span class=pl-c1>700</span>,<span class=pl-c1>600</span>)</td>
      </tr>
      <tr>
        <td id="L270" class="blob-num js-line-number" data-line-number="270"></td>
        <td id="LC270" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetFillColor</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L271" class="blob-num js-line-number" data-line-number="271"></td>
        <td id="LC271" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetBorderMode</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L272" class="blob-num js-line-number" data-line-number="272"></td>
        <td id="LC272" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetFrameFillStyle</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L273" class="blob-num js-line-number" data-line-number="273"></td>
        <td id="LC273" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetFrameBorderMode</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L274" class="blob-num js-line-number" data-line-number="274"></td>
        <td id="LC274" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetLeftMargin</span>( <span class=pl-c1>0.12</span> )</td>
      </tr>
      <tr>
        <td id="L275" class="blob-num js-line-number" data-line-number="275"></td>
        <td id="LC275" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetRightMargin</span>( <span class=pl-c1>0.9</span> )</td>
      </tr>
      <tr>
        <td id="L276" class="blob-num js-line-number" data-line-number="276"></td>
        <td id="LC276" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetTopMargin</span>( <span class=pl-c1>1</span> )</td>
      </tr>
      <tr>
        <td id="L277" class="blob-num js-line-number" data-line-number="277"></td>
        <td id="LC277" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetBottomMargin</span>(<span class=pl-c1>-</span><span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L278" class="blob-num js-line-number" data-line-number="278"></td>
        <td id="LC278" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetTickx</span>(<span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L279" class="blob-num js-line-number" data-line-number="279"></td>
        <td id="LC279" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>SetTicky</span>(<span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L280" class="blob-num js-line-number" data-line-number="280"></td>
        <td id="LC280" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-en>cd</span>()</td>
      </tr>
      <tr>
        <td id="L281" class="blob-num js-line-number" data-line-number="281"></td>
        <td id="LC281" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L282" class="blob-num js-line-number" data-line-number="282"></td>
        <td id="LC282" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span><span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TPad</span>(<span class=pl-s>&quot;pad1&quot;</span>, <span class=pl-s>&quot;pad1&quot;</span>, <span class=pl-c1>0</span>, <span class=pl-c1>0.31</span> , <span class=pl-c1>1</span>, <span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L283" class="blob-num js-line-number" data-line-number="283"></td>
        <td id="LC283" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>SetTopMargin</span>(<span class=pl-c1>0.1</span>)</td>
      </tr>
      <tr>
        <td id="L284" class="blob-num js-line-number" data-line-number="284"></td>
        <td id="LC284" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>SetBottomMargin</span>(<span class=pl-c1>0.02</span>)</td>
      </tr>
      <tr>
        <td id="L285" class="blob-num js-line-number" data-line-number="285"></td>
        <td id="LC285" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>SetLeftMargin</span>(<span class=pl-c1>0.12</span>)</td>
      </tr>
      <tr>
        <td id="L286" class="blob-num js-line-number" data-line-number="286"></td>
        <td id="LC286" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>SetRightMargin</span>(<span class=pl-c1>0.05</span>)</td>
      </tr>
      <tr>
        <td id="L287" class="blob-num js-line-number" data-line-number="287"></td>
        <td id="LC287" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>SetBorderMode</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L288" class="blob-num js-line-number" data-line-number="288"></td>
        <td id="LC288" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>SetTickx</span>(<span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L289" class="blob-num js-line-number" data-line-number="289"></td>
        <td id="LC289" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>SetTicky</span>(<span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L290" class="blob-num js-line-number" data-line-number="290"></td>
        <td id="LC290" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>Draw</span>()</td>
      </tr>
      <tr>
        <td id="L291" class="blob-num js-line-number" data-line-number="291"></td>
        <td id="LC291" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-en>cd</span>()</td>
      </tr>
      <tr>
        <td id="L292" class="blob-num js-line-number" data-line-number="292"></td>
        <td id="LC292" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-c1>not</span> <span class=pl-s1>blind</span>:</td>
      </tr>
      <tr>
        <td id="L293" class="blob-num js-line-number" data-line-number="293"></td>
        <td id="LC293" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>maximum</span> <span class=pl-c1>=</span> <span class=pl-en>max</span>(<span class=pl-s1>stack</span>.<span class=pl-v>GetMaximum</span>(),<span class=pl-s1>hdata</span>.<span class=pl-v>GetMaximum</span>())</td>
      </tr>
      <tr>
        <td id="L294" class="blob-num js-line-number" data-line-number="294"></td>
        <td id="LC294" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L295" class="blob-num js-line-number" data-line-number="295"></td>
        <td id="LC295" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>maximum</span> <span class=pl-c1>=</span> <span class=pl-s1>stack</span>.<span class=pl-v>GetMaximum</span>()</td>
      </tr>
      <tr>
        <td id="L296" class="blob-num js-line-number" data-line-number="296"></td>
        <td id="LC296" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>logscale</span> <span class=pl-c1>=</span> <span class=pl-c1>True</span> <span class=pl-c># False #</span></td>
      </tr>
      <tr>
        <td id="L297" class="blob-num js-line-number" data-line-number="297"></td>
        <td id="LC297" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span>(<span class=pl-s1>logscale</span>):</td>
      </tr>
      <tr>
        <td id="L298" class="blob-num js-line-number" data-line-number="298"></td>
        <td id="LC298" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>pad1</span>.<span class=pl-v>SetLogy</span>()</td>
      </tr>
      <tr>
        <td id="L299" class="blob-num js-line-number" data-line-number="299"></td>
        <td id="LC299" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>stack</span>.<span class=pl-v>SetMaximum</span>(<span class=pl-s1>maximum</span><span class=pl-c1>*</span><span class=pl-c1>1000</span>)</td>
      </tr>
      <tr>
        <td id="L300" class="blob-num js-line-number" data-line-number="300"></td>
        <td id="LC300" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L301" class="blob-num js-line-number" data-line-number="301"></td>
        <td id="LC301" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>stack</span>.<span class=pl-v>SetMaximum</span>(<span class=pl-s1>maximum</span><span class=pl-c1>*</span><span class=pl-c1>1.6</span>)</td>
      </tr>
      <tr>
        <td id="L302" class="blob-num js-line-number" data-line-number="302"></td>
        <td id="LC302" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>SetMinimum</span>(<span class=pl-c1>0.01</span>)</td>
      </tr>
      <tr>
        <td id="L303" class="blob-num js-line-number" data-line-number="303"></td>
        <td id="LC303" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-s1>opt</span>.<span class=pl-s1>tostack</span>:</td>
      </tr>
      <tr>
        <td id="L304" class="blob-num js-line-number" data-line-number="304"></td>
        <td id="LC304" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>stack</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;HIST&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L305" class="blob-num js-line-number" data-line-number="305"></td>
        <td id="LC305" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L306" class="blob-num js-line-number" data-line-number="306"></td>
        <td id="LC306" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>stack</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;HIST NOSTACK&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L307" class="blob-num js-line-number" data-line-number="307"></td>
        <td id="LC307" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>step</span> <span class=pl-c1>=</span> <span class=pl-en>float</span>(<span class=pl-s1>variabile_</span>.<span class=pl-s1>_xmax</span> <span class=pl-c1>-</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_xmin</span>)<span class=pl-c1>/</span><span class=pl-en>float</span>(<span class=pl-s1>variabile_</span>.<span class=pl-s1>_nbins</span>)</td>
      </tr>
      <tr>
        <td id="L308" class="blob-num js-line-number" data-line-number="308"></td>
        <td id="LC308" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>print</span> <span class=pl-en>str</span>(<span class=pl-s1>step</span>)</td>
      </tr>
      <tr>
        <td id="L309" class="blob-num js-line-number" data-line-number="309"></td>
        <td id="LC309" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-s>&quot;GeV&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>variabile_</span>.<span class=pl-s1>_title</span>:</td>
      </tr>
      <tr>
        <td id="L310" class="blob-num js-line-number" data-line-number="310"></td>
        <td id="LC310" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span> <span class=pl-s1>step</span>.<span class=pl-en>is_integer</span>():</td>
      </tr>
      <tr>
        <td id="L311" class="blob-num js-line-number" data-line-number="311"></td>
        <td id="LC311" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>ytitle</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;Events / %.0f GeV&quot;</span> <span class=pl-c1>%</span><span class=pl-s1>step</span></td>
      </tr>
      <tr>
        <td id="L312" class="blob-num js-line-number" data-line-number="312"></td>
        <td id="LC312" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L313" class="blob-num js-line-number" data-line-number="313"></td>
        <td id="LC313" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>ytitle</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;Events / %.2f GeV&quot;</span> <span class=pl-c1>%</span><span class=pl-s1>step</span></td>
      </tr>
      <tr>
        <td id="L314" class="blob-num js-line-number" data-line-number="314"></td>
        <td id="LC314" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L315" class="blob-num js-line-number" data-line-number="315"></td>
        <td id="LC315" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span> <span class=pl-s1>step</span>.<span class=pl-en>is_integer</span>():</td>
      </tr>
      <tr>
        <td id="L316" class="blob-num js-line-number" data-line-number="316"></td>
        <td id="LC316" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>ytitle</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;Events / %.0f units&quot;</span> <span class=pl-c1>%</span><span class=pl-s1>step</span></td>
      </tr>
      <tr>
        <td id="L317" class="blob-num js-line-number" data-line-number="317"></td>
        <td id="LC317" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L318" class="blob-num js-line-number" data-line-number="318"></td>
        <td id="LC318" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>ytitle</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;Events / %.2f units&quot;</span> <span class=pl-c1>%</span><span class=pl-s1>step</span></td>
      </tr>
      <tr>
        <td id="L319" class="blob-num js-line-number" data-line-number="319"></td>
        <td id="LC319" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetTitle</span>(<span class=pl-s1>ytitle</span>)</td>
      </tr>
      <tr>
        <td id="L320" class="blob-num js-line-number" data-line-number="320"></td>
        <td id="LC320" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetTitleFont</span>(<span class=pl-c1>42</span>)</td>
      </tr>
      <tr>
        <td id="L321" class="blob-num js-line-number" data-line-number="321"></td>
        <td id="LC321" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetLabelOffset</span>(<span class=pl-c1>1.8</span>)</td>
      </tr>
      <tr>
        <td id="L322" class="blob-num js-line-number" data-line-number="322"></td>
        <td id="LC322" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetTitleOffset</span>(<span class=pl-c1>0.85</span>)</td>
      </tr>
      <tr>
        <td id="L323" class="blob-num js-line-number" data-line-number="323"></td>
        <td id="LC323" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetLabelSize</span>(<span class=pl-c1>0.15</span>)</td>
      </tr>
      <tr>
        <td id="L324" class="blob-num js-line-number" data-line-number="324"></td>
        <td id="LC324" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetLabelSize</span>(<span class=pl-c1>0.07</span>)</td>
      </tr>
      <tr>
        <td id="L325" class="blob-num js-line-number" data-line-number="325"></td>
        <td id="LC325" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetTitleSize</span>(<span class=pl-c1>0.07</span>)</td>
      </tr>
      <tr>
        <td id="L326" class="blob-num js-line-number" data-line-number="326"></td>
        <td id="LC326" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>SetTitle</span>(<span class=pl-s>&quot;&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L327" class="blob-num js-line-number" data-line-number="327"></td>
        <td id="LC327" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span>(<span class=pl-s1>signal</span>):</td>
      </tr>
      <tr>
        <td id="L328" class="blob-num js-line-number" data-line-number="328"></td>
        <td id="LC328" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>for</span> <span class=pl-s1>hsig</span> <span class=pl-c1>in</span> <span class=pl-s1>h_sig</span>:</td>
      </tr>
      <tr>
        <td id="L329" class="blob-num js-line-number" data-line-number="329"></td>
        <td id="LC329" class="blob-code blob-code-inner js-file-line">               <span class=pl-c>#hsig.Scale(1000)</span></td>
      </tr>
      <tr>
        <td id="L330" class="blob-num js-line-number" data-line-number="330"></td>
        <td id="LC330" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>hsig</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;same L&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L331" class="blob-num js-line-number" data-line-number="331"></td>
        <td id="LC331" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>leg_stack</span>.<span class=pl-v>AddEntry</span>(<span class=pl-s1>hsig</span>, <span class=pl-s1>hsig</span>.<span class=pl-v>GetName</span>(), <span class=pl-s>&quot;l&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L332" class="blob-num js-line-number" data-line-number="332"></td>
        <td id="LC332" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_err</span> <span class=pl-c1>=</span> <span class=pl-s1>stack</span>.<span class=pl-v>GetStack</span>().<span class=pl-v>Last</span>().<span class=pl-v>Clone</span>(<span class=pl-s>&quot;h_err&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L333" class="blob-num js-line-number" data-line-number="333"></td>
        <td id="LC333" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_err</span>.<span class=pl-v>SetLineWidth</span>(<span class=pl-c1>100</span>)</td>
      </tr>
      <tr>
        <td id="L334" class="blob-num js-line-number" data-line-number="334"></td>
        <td id="LC334" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_err</span>.<span class=pl-v>SetFillStyle</span>(<span class=pl-c1>3154</span>)</td>
      </tr>
      <tr>
        <td id="L335" class="blob-num js-line-number" data-line-number="335"></td>
        <td id="LC335" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_err</span>.<span class=pl-v>SetMarkerSize</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L336" class="blob-num js-line-number" data-line-number="336"></td>
        <td id="LC336" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_err</span>.<span class=pl-v>SetFillColor</span>(<span class=pl-v>ROOT</span>.<span class=pl-s1>kGray</span><span class=pl-c1>+</span><span class=pl-c1>2</span>)</td>
      </tr>
      <tr>
        <td id="L337" class="blob-num js-line-number" data-line-number="337"></td>
        <td id="LC337" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_err</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;e2same0&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L338" class="blob-num js-line-number" data-line-number="338"></td>
        <td id="LC338" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span>.<span class=pl-v>AddEntry</span>(<span class=pl-s1>h_err</span>, <span class=pl-s>&quot;Stat. Unc.&quot;</span>, <span class=pl-s>&quot;f&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L339" class="blob-num js-line-number" data-line-number="339"></td>
        <td id="LC339" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-c1>not</span> <span class=pl-s1>blind</span>: </td>
      </tr>
      <tr>
        <td id="L340" class="blob-num js-line-number" data-line-number="340"></td>
        <td id="LC340" class="blob-code blob-code-inner js-file-line">          <span class=pl-en>print</span>(<span class=pl-s1>hdata</span>.<span class=pl-v>Integral</span>())</td>
      </tr>
      <tr>
        <td id="L341" class="blob-num js-line-number" data-line-number="341"></td>
        <td id="LC341" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>hdata</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;eSAMEpx0&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L342" class="blob-num js-line-number" data-line-number="342"></td>
        <td id="LC342" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L343" class="blob-num js-line-number" data-line-number="343"></td>
        <td id="LC343" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>hdata</span> <span class=pl-c1>=</span> <span class=pl-s1>stack</span>.<span class=pl-v>GetStack</span>().<span class=pl-v>Last</span>().<span class=pl-v>Clone</span>(<span class=pl-s>&quot;h_data&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L344" class="blob-num js-line-number" data-line-number="344"></td>
        <td id="LC344" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>leg_stack</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;same&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L345" class="blob-num js-line-number" data-line-number="345"></td>
        <td id="LC345" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L346" class="blob-num js-line-number" data-line-number="346"></td>
        <td id="LC346" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>CMS_lumi</span>.<span class=pl-s1>writeExtraText</span> <span class=pl-c1>=</span> <span class=pl-c1>1</span></td>
      </tr>
      <tr>
        <td id="L347" class="blob-num js-line-number" data-line-number="347"></td>
        <td id="LC347" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>CMS_lumi</span>.<span class=pl-s1>extraText</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;&quot;</span></td>
      </tr>
      <tr>
        <td id="L348" class="blob-num js-line-number" data-line-number="348"></td>
        <td id="LC348" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-en>str</span>(<span class=pl-s1>lep_</span>).<span class=pl-en>strip</span>(<span class=pl-s>&#39;[]&#39;</span>) <span class=pl-c1>==</span> <span class=pl-s>&quot;muon&quot;</span>:</td>
      </tr>
      <tr>
        <td id="L349" class="blob-num js-line-number" data-line-number="349"></td>
        <td id="LC349" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>lep_tag</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;#mu+&quot;</span></td>
      </tr>
      <tr>
        <td id="L350" class="blob-num js-line-number" data-line-number="350"></td>
        <td id="LC350" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>elif</span> <span class=pl-en>str</span>(<span class=pl-s1>lep_</span>).<span class=pl-en>strip</span>(<span class=pl-s>&#39;[]&#39;</span>) <span class=pl-c1>==</span> <span class=pl-s>&quot;electron&quot;</span>:</td>
      </tr>
      <tr>
        <td id="L351" class="blob-num js-line-number" data-line-number="351"></td>
        <td id="LC351" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>lep_tag</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;e+&quot;</span></td>
      </tr>
      <tr>
        <td id="L352" class="blob-num js-line-number" data-line-number="352"></td>
        <td id="LC352" class="blob-code blob-code-inner js-file-line">          </td>
      </tr>
      <tr>
        <td id="L353" class="blob-num js-line-number" data-line-number="353"></td>
        <td id="LC353" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>lumi_sqrtS</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;%s fb^{-1}  (13 TeV)&quot;</span><span class=pl-c1>%</span>(<span class=pl-s1>lumi</span>)</td>
      </tr>
      <tr>
        <td id="L354" class="blob-num js-line-number" data-line-number="354"></td>
        <td id="LC354" class="blob-code blob-code-inner js-file-line">     </td>
      </tr>
      <tr>
        <td id="L355" class="blob-num js-line-number" data-line-number="355"></td>
        <td id="LC355" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>iPeriod</span> <span class=pl-c1>=</span> <span class=pl-c1>0</span></td>
      </tr>
      <tr>
        <td id="L356" class="blob-num js-line-number" data-line-number="356"></td>
        <td id="LC356" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>iPos</span> <span class=pl-c1>=</span> <span class=pl-c1>11</span></td>
      </tr>
      <tr>
        <td id="L357" class="blob-num js-line-number" data-line-number="357"></td>
        <td id="LC357" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>CMS_lumi</span>(<span class=pl-s1>pad1</span>, <span class=pl-s1>lumi_sqrtS</span>, <span class=pl-s1>iPos</span>, <span class=pl-s1>lep_tag</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>reg_</span>))</td>
      </tr>
      <tr>
        <td id="L358" class="blob-num js-line-number" data-line-number="358"></td>
        <td id="LC358" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>hratio</span> <span class=pl-c1>=</span> <span class=pl-s1>stack</span>.<span class=pl-v>GetStack</span>().<span class=pl-v>Last</span>()</td>
      </tr>
      <tr>
        <td id="L359" class="blob-num js-line-number" data-line-number="359"></td>
        <td id="LC359" class="blob-code blob-code-inner js-file-line">     </td>
      </tr>
      <tr>
        <td id="L360" class="blob-num js-line-number" data-line-number="360"></td>
        <td id="LC360" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-en>cd</span>()</td>
      </tr>
      <tr>
        <td id="L361" class="blob-num js-line-number" data-line-number="361"></td>
        <td id="LC361" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span><span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TPad</span>(<span class=pl-s>&quot;pad2&quot;</span>, <span class=pl-s>&quot;pad2&quot;</span>, <span class=pl-c1>0</span>, <span class=pl-c1>0.01</span> , <span class=pl-c1>1</span>, <span class=pl-c1>0.30</span>)</td>
      </tr>
      <tr>
        <td id="L362" class="blob-num js-line-number" data-line-number="362"></td>
        <td id="LC362" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span>.<span class=pl-v>SetTopMargin</span>(<span class=pl-c1>0.05</span>)</td>
      </tr>
      <tr>
        <td id="L363" class="blob-num js-line-number" data-line-number="363"></td>
        <td id="LC363" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span>.<span class=pl-v>SetBottomMargin</span>(<span class=pl-c1>0.45</span>)</td>
      </tr>
      <tr>
        <td id="L364" class="blob-num js-line-number" data-line-number="364"></td>
        <td id="LC364" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span>.<span class=pl-v>SetLeftMargin</span>(<span class=pl-c1>0.12</span>)</td>
      </tr>
      <tr>
        <td id="L365" class="blob-num js-line-number" data-line-number="365"></td>
        <td id="LC365" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span>.<span class=pl-v>SetRightMargin</span>(<span class=pl-c1>0.05</span>)</td>
      </tr>
      <tr>
        <td id="L366" class="blob-num js-line-number" data-line-number="366"></td>
        <td id="LC366" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>ROOT</span>.<span class=pl-s1>gStyle</span>.<span class=pl-v>SetHatchesSpacing</span>(<span class=pl-c1>2</span>)</td>
      </tr>
      <tr>
        <td id="L367" class="blob-num js-line-number" data-line-number="367"></td>
        <td id="LC367" class="blob-code blob-code-inner js-file-line">     <span class=pl-v>ROOT</span>.<span class=pl-s1>gStyle</span>.<span class=pl-v>SetHatchesLineWidth</span>(<span class=pl-c1>2</span>)</td>
      </tr>
      <tr>
        <td id="L368" class="blob-num js-line-number" data-line-number="368"></td>
        <td id="LC368" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-en>cd</span>()</td>
      </tr>
      <tr>
        <td id="L369" class="blob-num js-line-number" data-line-number="369"></td>
        <td id="LC369" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span>.<span class=pl-v>Draw</span>()</td>
      </tr>
      <tr>
        <td id="L370" class="blob-num js-line-number" data-line-number="370"></td>
        <td id="LC370" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span>.<span class=pl-en>cd</span>()</td>
      </tr>
      <tr>
        <td id="L371" class="blob-num js-line-number" data-line-number="371"></td>
        <td id="LC371" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span> <span class=pl-c1>=</span> <span class=pl-s1>hdata</span>.<span class=pl-v>Clone</span>(<span class=pl-s>&quot;ratio&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L372" class="blob-num js-line-number" data-line-number="372"></td>
        <td id="LC372" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>SetLineColor</span>(<span class=pl-v>ROOT</span>.<span class=pl-s1>kBlack</span>)</td>
      </tr>
      <tr>
        <td id="L373" class="blob-num js-line-number" data-line-number="373"></td>
        <td id="LC373" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>SetMaximum</span>(<span class=pl-c1>2</span>)</td>
      </tr>
      <tr>
        <td id="L374" class="blob-num js-line-number" data-line-number="374"></td>
        <td id="LC374" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>SetMinimum</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L375" class="blob-num js-line-number" data-line-number="375"></td>
        <td id="LC375" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>Sumw2</span>()</td>
      </tr>
      <tr>
        <td id="L376" class="blob-num js-line-number" data-line-number="376"></td>
        <td id="LC376" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>SetStats</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L377" class="blob-num js-line-number" data-line-number="377"></td>
        <td id="LC377" class="blob-code blob-code-inner js-file-line">     </td>
      </tr>
      <tr>
        <td id="L378" class="blob-num js-line-number" data-line-number="378"></td>
        <td id="LC378" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>Divide</span>(<span class=pl-s1>hratio</span>)</td>
      </tr>
      <tr>
        <td id="L379" class="blob-num js-line-number" data-line-number="379"></td>
        <td id="LC379" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>SetMarkerStyle</span>(<span class=pl-c1>20</span>)</td>
      </tr>
      <tr>
        <td id="L380" class="blob-num js-line-number" data-line-number="380"></td>
        <td id="LC380" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>SetMarkerSize</span>(<span class=pl-c1>0.9</span>)</td>
      </tr>
      <tr>
        <td id="L381" class="blob-num js-line-number" data-line-number="381"></td>
        <td id="LC381" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;epx0e0&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L382" class="blob-num js-line-number" data-line-number="382"></td>
        <td id="LC382" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>SetTitle</span>(<span class=pl-s>&quot;&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L383" class="blob-num js-line-number" data-line-number="383"></td>
        <td id="LC383" class="blob-code blob-code-inner js-file-line">     </td>
      </tr>
      <tr>
        <td id="L384" class="blob-num js-line-number" data-line-number="384"></td>
        <td id="LC384" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span> <span class=pl-c1>=</span> <span class=pl-s1>hratio</span>.<span class=pl-v>Clone</span>(<span class=pl-s>&quot;h_err&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L385" class="blob-num js-line-number" data-line-number="385"></td>
        <td id="LC385" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>Reset</span>()</td>
      </tr>
      <tr>
        <td id="L386" class="blob-num js-line-number" data-line-number="386"></td>
        <td id="LC386" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>Sumw2</span>()</td>
      </tr>
      <tr>
        <td id="L387" class="blob-num js-line-number" data-line-number="387"></td>
        <td id="LC387" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>i</span> <span class=pl-c1>in</span> <span class=pl-en>range</span>(<span class=pl-c1>1</span>,<span class=pl-s1>hratio</span>.<span class=pl-v>GetNbinsX</span>()<span class=pl-c1>+</span><span class=pl-c1>1</span>):</td>
      </tr>
      <tr>
        <td id="L388" class="blob-num js-line-number" data-line-number="388"></td>
        <td id="LC388" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>SetBinContent</span>(<span class=pl-s1>i</span>,<span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L389" class="blob-num js-line-number" data-line-number="389"></td>
        <td id="LC389" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s1>hratio</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-s1>i</span>)):</td>
      </tr>
      <tr>
        <td id="L390" class="blob-num js-line-number" data-line-number="390"></td>
        <td id="LC390" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>SetBinError</span>(<span class=pl-s1>i</span>, (<span class=pl-s1>hratio</span>.<span class=pl-v>GetBinError</span>(<span class=pl-s1>i</span>)<span class=pl-c1>/</span><span class=pl-s1>hratio</span>.<span class=pl-v>GetBinContent</span>(<span class=pl-s1>i</span>)))</td>
      </tr>
      <tr>
        <td id="L391" class="blob-num js-line-number" data-line-number="391"></td>
        <td id="LC391" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L392" class="blob-num js-line-number" data-line-number="392"></td>
        <td id="LC392" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>SetBinError</span>(<span class=pl-s1>i</span>, <span class=pl-c1>10</span><span class=pl-c1>^</span>(<span class=pl-c1>-</span><span class=pl-c1>99</span>))</td>
      </tr>
      <tr>
        <td id="L393" class="blob-num js-line-number" data-line-number="393"></td>
        <td id="LC393" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>SetLineWidth</span>(<span class=pl-c1>100</span>)</td>
      </tr>
      <tr>
        <td id="L394" class="blob-num js-line-number" data-line-number="394"></td>
        <td id="LC394" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L395" class="blob-num js-line-number" data-line-number="395"></td>
        <td id="LC395" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>SetMarkerSize</span>(<span class=pl-c1>0</span>)</td>
      </tr>
      <tr>
        <td id="L396" class="blob-num js-line-number" data-line-number="396"></td>
        <td id="LC396" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>SetFillColor</span>(<span class=pl-v>ROOT</span>.<span class=pl-s1>kGray</span><span class=pl-c1>+</span><span class=pl-c1>1</span>)</td>
      </tr>
      <tr>
        <td id="L397" class="blob-num js-line-number" data-line-number="397"></td>
        <td id="LC397" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;e20same&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L398" class="blob-num js-line-number" data-line-number="398"></td>
        <td id="LC398" class="blob-code blob-code-inner js-file-line">     </td>
      </tr>
      <tr>
        <td id="L399" class="blob-num js-line-number" data-line-number="399"></td>
        <td id="LC399" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>f1</span> <span class=pl-c1>=</span> <span class=pl-v>ROOT</span>.<span class=pl-v>TLine</span>(<span class=pl-s1>variabile_</span>.<span class=pl-s1>_xmin</span>, <span class=pl-c1>1.</span>, <span class=pl-s1>variabile_</span>.<span class=pl-s1>_xmax</span>,<span class=pl-c1>1.</span>)</td>
      </tr>
      <tr>
        <td id="L400" class="blob-num js-line-number" data-line-number="400"></td>
        <td id="LC400" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>f1</span>.<span class=pl-v>SetLineColor</span>(<span class=pl-v>ROOT</span>.<span class=pl-s1>kBlack</span>)</td>
      </tr>
      <tr>
        <td id="L401" class="blob-num js-line-number" data-line-number="401"></td>
        <td id="LC401" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>f1</span>.<span class=pl-v>SetLineStyle</span>(<span class=pl-v>ROOT</span>.<span class=pl-s1>kDashed</span>)</td>
      </tr>
      <tr>
        <td id="L402" class="blob-num js-line-number" data-line-number="402"></td>
        <td id="LC402" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>f1</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;same&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L403" class="blob-num js-line-number" data-line-number="403"></td>
        <td id="LC403" class="blob-code blob-code-inner js-file-line">     </td>
      </tr>
      <tr>
        <td id="L404" class="blob-num js-line-number" data-line-number="404"></td>
        <td id="LC404" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetTitle</span>(<span class=pl-s>&quot;Data / MC&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L405" class="blob-num js-line-number" data-line-number="405"></td>
        <td id="LC405" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetNdivisions</span>(<span class=pl-c1>503</span>)</td>
      </tr>
      <tr>
        <td id="L406" class="blob-num js-line-number" data-line-number="406"></td>
        <td id="LC406" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetLabelFont</span>(<span class=pl-c1>42</span>)</td>
      </tr>
      <tr>
        <td id="L407" class="blob-num js-line-number" data-line-number="407"></td>
        <td id="LC407" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetLabelFont</span>(<span class=pl-c1>42</span>)</td>
      </tr>
      <tr>
        <td id="L408" class="blob-num js-line-number" data-line-number="408"></td>
        <td id="LC408" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetTitleFont</span>(<span class=pl-c1>42</span>)</td>
      </tr>
      <tr>
        <td id="L409" class="blob-num js-line-number" data-line-number="409"></td>
        <td id="LC409" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetTitleFont</span>(<span class=pl-c1>42</span>)</td>
      </tr>
      <tr>
        <td id="L410" class="blob-num js-line-number" data-line-number="410"></td>
        <td id="LC410" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetTitleOffset</span>(<span class=pl-c1>1.1</span>)</td>
      </tr>
      <tr>
        <td id="L411" class="blob-num js-line-number" data-line-number="411"></td>
        <td id="LC411" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetTitleOffset</span>(<span class=pl-c1>0.35</span>)</td>
      </tr>
      <tr>
        <td id="L412" class="blob-num js-line-number" data-line-number="412"></td>
        <td id="LC412" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetLabelSize</span>(<span class=pl-c1>0.15</span>)</td>
      </tr>
      <tr>
        <td id="L413" class="blob-num js-line-number" data-line-number="413"></td>
        <td id="LC413" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetLabelSize</span>(<span class=pl-c1>0.15</span>)</td>
      </tr>
      <tr>
        <td id="L414" class="blob-num js-line-number" data-line-number="414"></td>
        <td id="LC414" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetTitleSize</span>(<span class=pl-c1>0.16</span>)</td>
      </tr>
      <tr>
        <td id="L415" class="blob-num js-line-number" data-line-number="415"></td>
        <td id="LC415" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetTitleSize</span>(<span class=pl-c1>0.16</span>)</td>
      </tr>
      <tr>
        <td id="L416" class="blob-num js-line-number" data-line-number="416"></td>
        <td id="LC416" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetRangeUser</span>(<span class=pl-c1>0.</span>,<span class=pl-c1>2.0</span>)</td>
      </tr>
      <tr>
        <td id="L417" class="blob-num js-line-number" data-line-number="417"></td>
        <td id="LC417" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetTitle</span>(<span class=pl-s1>variabile_</span>.<span class=pl-s1>_title</span>)</td>
      </tr>
      <tr>
        <td id="L418" class="blob-num js-line-number" data-line-number="418"></td>
        <td id="LC418" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetXaxis</span>().<span class=pl-v>SetLabelOffset</span>(<span class=pl-c1>0.04</span>)</td>
      </tr>
      <tr>
        <td id="L419" class="blob-num js-line-number" data-line-number="419"></td>
        <td id="LC419" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>GetYaxis</span>().<span class=pl-v>SetLabelOffset</span>(<span class=pl-c1>0.02</span>)</td>
      </tr>
      <tr>
        <td id="L420" class="blob-num js-line-number" data-line-number="420"></td>
        <td id="LC420" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>ratio</span>.<span class=pl-v>Draw</span>(<span class=pl-s>&quot;epx0e0same&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L421" class="blob-num js-line-number" data-line-number="421"></td>
        <td id="LC421" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L422" class="blob-num js-line-number" data-line-number="422"></td>
        <td id="LC422" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-en>cd</span>()</td>
      </tr>
      <tr>
        <td id="L423" class="blob-num js-line-number" data-line-number="423"></td>
        <td id="LC423" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#ROOT.TGaxis.SetMaxDigits(3)</span></td>
      </tr>
      <tr>
        <td id="L424" class="blob-num js-line-number" data-line-number="424"></td>
        <td id="LC424" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>RedrawAxis</span>()</td>
      </tr>
      <tr>
        <td id="L425" class="blob-num js-line-number" data-line-number="425"></td>
        <td id="LC425" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span>.<span class=pl-v>RedrawAxis</span>()</td>
      </tr>
      <tr>
        <td id="L426" class="blob-num js-line-number" data-line-number="426"></td>
        <td id="LC426" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>Update</span>()</td>
      </tr>
      <tr>
        <td id="L427" class="blob-num js-line-number" data-line-number="427"></td>
        <td id="LC427" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#c1.Print(&quot;stack/&quot;+canvasname+&quot;.pdf&quot;)</span></td>
      </tr>
      <tr>
        <td id="L428" class="blob-num js-line-number" data-line-number="428"></td>
        <td id="LC428" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>Print</span>(<span class=pl-s1>plotrepo</span> <span class=pl-c1>+</span> <span class=pl-s>&quot;stack/&quot;</span><span class=pl-c1>+</span><span class=pl-s1>canvasname</span><span class=pl-c1>+</span><span class=pl-s>&quot;.png&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L429" class="blob-num js-line-number" data-line-number="429"></td>
        <td id="LC429" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>histo</span></td>
      </tr>
      <tr>
        <td id="L430" class="blob-num js-line-number" data-line-number="430"></td>
        <td id="LC430" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>tmp</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L431" class="blob-num js-line-number" data-line-number="431"></td>
        <td id="LC431" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L432" class="blob-num js-line-number" data-line-number="432"></td>
        <td id="LC432" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>tmp</span></td>
      </tr>
      <tr>
        <td id="L433" class="blob-num js-line-number" data-line-number="433"></td>
        <td id="LC433" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>h</span></td>
      </tr>
      <tr>
        <td id="L434" class="blob-num js-line-number" data-line-number="434"></td>
        <td id="LC434" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>h_sig</span></td>
      </tr>
      <tr>
        <td id="L435" class="blob-num js-line-number" data-line-number="435"></td>
        <td id="LC435" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_err</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L436" class="blob-num js-line-number" data-line-number="436"></td>
        <td id="LC436" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>h_err</span></td>
      </tr>
      <tr>
        <td id="L437" class="blob-num js-line-number" data-line-number="437"></td>
        <td id="LC437" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>h_bkg_err</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L438" class="blob-num js-line-number" data-line-number="438"></td>
        <td id="LC438" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>h_bkg_err</span></td>
      </tr>
      <tr>
        <td id="L439" class="blob-num js-line-number" data-line-number="439"></td>
        <td id="LC439" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>hratio</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L440" class="blob-num js-line-number" data-line-number="440"></td>
        <td id="LC440" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>hratio</span></td>
      </tr>
      <tr>
        <td id="L441" class="blob-num js-line-number" data-line-number="441"></td>
        <td id="LC441" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>stack</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L442" class="blob-num js-line-number" data-line-number="442"></td>
        <td id="LC442" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>stack</span></td>
      </tr>
      <tr>
        <td id="L443" class="blob-num js-line-number" data-line-number="443"></td>
        <td id="LC443" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad1</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L444" class="blob-num js-line-number" data-line-number="444"></td>
        <td id="LC444" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>pad1</span></td>
      </tr>
      <tr>
        <td id="L445" class="blob-num js-line-number" data-line-number="445"></td>
        <td id="LC445" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>pad2</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L446" class="blob-num js-line-number" data-line-number="446"></td>
        <td id="LC446" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>pad2</span></td>
      </tr>
      <tr>
        <td id="L447" class="blob-num js-line-number" data-line-number="447"></td>
        <td id="LC447" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>c1</span>.<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L448" class="blob-num js-line-number" data-line-number="448"></td>
        <td id="LC448" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>del</span> <span class=pl-s1>c1</span></td>
      </tr>
      <tr>
        <td id="L449" class="blob-num js-line-number" data-line-number="449"></td>
        <td id="LC449" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>s</span> <span class=pl-c1>in</span> <span class=pl-s1>samples_</span>:</td>
      </tr>
      <tr>
        <td id="L450" class="blob-num js-line-number" data-line-number="450"></td>
        <td id="LC450" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>infile</span>[<span class=pl-s1>s</span>.<span class=pl-s1>label</span>].<span class=pl-v>Close</span>()</td>
      </tr>
      <tr>
        <td id="L451" class="blob-num js-line-number" data-line-number="451"></td>
        <td id="LC451" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>infile</span>[<span class=pl-s1>s</span>.<span class=pl-s1>label</span>].<span class=pl-v>Delete</span>()</td>
      </tr>
      <tr>
        <td id="L452" class="blob-num js-line-number" data-line-number="452"></td>
        <td id="LC452" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>os</span>.<span class=pl-en>system</span>(<span class=pl-s>&#39;set LD_PRELOAD=libtcmalloc.so&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L453" class="blob-num js-line-number" data-line-number="453"></td>
        <td id="LC453" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L454" class="blob-num js-line-number" data-line-number="454"></td>
        <td id="LC454" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>dataset_dict</span> <span class=pl-c1>=</span> {<span class=pl-s>&#39;2016&#39;</span>:[],<span class=pl-s>&#39;2017&#39;</span>:[],<span class=pl-s>&#39;2018&#39;</span>:[]}</td>
      </tr>
      <tr>
        <td id="L455" class="blob-num js-line-number" data-line-number="455"></td>
        <td id="LC455" class="blob-code blob-code-inner js-file-line"><span class=pl-k>if</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>dat</span><span class=pl-c1>!=</span> <span class=pl-s>&#39;all&#39;</span>):</td>
      </tr>
      <tr>
        <td id="L456" class="blob-num js-line-number" data-line-number="456"></td>
        <td id="LC456" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-c1>not</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>dat</span> <span class=pl-c1>in</span> <span class=pl-s1>sample_dict</span>.<span class=pl-en>keys</span>()):</td>
      </tr>
      <tr>
        <td id="L457" class="blob-num js-line-number" data-line-number="457"></td>
        <td id="LC457" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>print</span> <span class=pl-s1>sample_dict</span>.<span class=pl-en>keys</span>()</td>
      </tr>
      <tr>
        <td id="L458" class="blob-num js-line-number" data-line-number="458"></td>
        <td id="LC458" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>dataset_names</span> <span class=pl-c1>=</span> <span class=pl-en>map</span>(<span class=pl-s1>str</span>, <span class=pl-s1>opt</span>.<span class=pl-s1>dat</span>.<span class=pl-en>strip</span>(<span class=pl-s>&#39;[]&#39;</span>).<span class=pl-en>split</span>(<span class=pl-s>&#39;,&#39;</span>))</td>
      </tr>
      <tr>
        <td id="L459" class="blob-num js-line-number" data-line-number="459"></td>
        <td id="LC459" class="blob-code blob-code-inner js-file-line">     <span class=pl-c>#print dataset_names.keys()</span></td>
      </tr>
      <tr>
        <td id="L460" class="blob-num js-line-number" data-line-number="460"></td>
        <td id="LC460" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>samples</span> <span class=pl-c1>=</span> []</td>
      </tr>
      <tr>
        <td id="L461" class="blob-num js-line-number" data-line-number="461"></td>
        <td id="LC461" class="blob-code blob-code-inner js-file-line">     [<span class=pl-s1>samples</span>.<span class=pl-en>append</span>(<span class=pl-s1>sample_dict</span>[<span class=pl-s1>dataset_name</span>]) <span class=pl-k>for</span> <span class=pl-s1>dataset_name</span> <span class=pl-c1>in</span> <span class=pl-s1>dataset_names</span>]</td>
      </tr>
      <tr>
        <td id="L462" class="blob-num js-line-number" data-line-number="462"></td>
        <td id="LC462" class="blob-code blob-code-inner js-file-line">     [<span class=pl-s1>dataset_dict</span>[<span class=pl-en>str</span>(<span class=pl-s1>sample</span>.<span class=pl-s1>year</span>)].<span class=pl-en>append</span>(<span class=pl-s1>sample</span>) <span class=pl-k>for</span> <span class=pl-s1>sample</span> <span class=pl-c1>in</span> <span class=pl-s1>samples</span>]</td>
      </tr>
      <tr>
        <td id="L463" class="blob-num js-line-number" data-line-number="463"></td>
        <td id="LC463" class="blob-code blob-code-inner js-file-line"><span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L464" class="blob-num js-line-number" data-line-number="464"></td>
        <td id="LC464" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>dataset_dict</span> <span class=pl-c1>=</span> {</td>
      </tr>
      <tr>
        <td id="L465" class="blob-num js-line-number" data-line-number="465"></td>
        <td id="LC465" class="blob-code blob-code-inner js-file-line">          <span class=pl-s>&#39;2016&#39;</span>:[<span class=pl-v>DataMu_2016</span>, <span class=pl-v>DataEle_2016</span>, <span class=pl-v>DataHT_2016</span>, <span class=pl-v>ST_2016</span>, <span class=pl-v>QCD_2016</span>, <span class=pl-v>TT_Mtt_2016</span>, <span class=pl-v>WJets_2016</span>, <span class=pl-v>WP_M2000W20_RH_2016</span>, <span class=pl-v>WP_M3000W30_RH_2016</span>, <span class=pl-v>WP_M4000W40_RH_2016</span>, <span class=pl-v>WP_M4000W400_RH_2016</span>],</td>
      </tr>
      <tr>
        <td id="L466" class="blob-num js-line-number" data-line-number="466"></td>
        <td id="LC466" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#&#39;2016&#39;:[DataHTG_2016, DataMuG_2016, ST_2016, QCD_2016, TT_Mtt_2016, WJets_2016, WP_M2000W20_RH_2016, WP_M3000W30_RH_2016, WP_M4000W40_RH_2016, WP_M4000W400_RH_2016],</span></td>
      </tr>
      <tr>
        <td id="L467" class="blob-num js-line-number" data-line-number="467"></td>
        <td id="LC467" class="blob-code blob-code-inner js-file-line">          <span class=pl-s>&#39;2017&#39;</span>:[<span class=pl-v>DataMu_2017</span>, <span class=pl-v>DataEle_2017</span>, <span class=pl-v>DataHT_2017</span>, <span class=pl-v>ST_2017</span>, <span class=pl-v>QCD_2017</span>, <span class=pl-v>TT_Mtt_2017</span>, <span class=pl-v>WJets_2017</span>, <span class=pl-v>WP_M2000W20_RH_2017</span>, <span class=pl-v>WP_M3000W30_RH_2017</span>, <span class=pl-v>WP_M4000W40_RH_2017</span>, <span class=pl-v>WP_M4000W400_RH_2017</span>],</td>
      </tr>
      <tr>
        <td id="L468" class="blob-num js-line-number" data-line-number="468"></td>
        <td id="LC468" class="blob-code blob-code-inner js-file-line">          <span class=pl-s>&#39;2018&#39;</span>:[<span class=pl-v>DataMu_2018</span>, <span class=pl-v>DataEle_2018</span>, <span class=pl-v>TT_Mtt_2018</span>, <span class=pl-v>WJets_2018</span>]}</td>
      </tr>
      <tr>
        <td id="L469" class="blob-num js-line-number" data-line-number="469"></td>
        <td id="LC469" class="blob-code blob-code-inner js-file-line"><span class=pl-c>#print(dataset_dict.keys())</span></td>
      </tr>
      <tr>
        <td id="L470" class="blob-num js-line-number" data-line-number="470"></td>
        <td id="LC470" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L471" class="blob-num js-line-number" data-line-number="471"></td>
        <td id="LC471" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>years</span> <span class=pl-c1>=</span> []</td>
      </tr>
      <tr>
        <td id="L472" class="blob-num js-line-number" data-line-number="472"></td>
        <td id="LC472" class="blob-code blob-code-inner js-file-line"><span class=pl-k>if</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>year</span><span class=pl-c1>!=</span><span class=pl-s>&#39;all&#39;</span>):</td>
      </tr>
      <tr>
        <td id="L473" class="blob-num js-line-number" data-line-number="473"></td>
        <td id="LC473" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>years</span> <span class=pl-c1>=</span> <span class=pl-en>map</span>(<span class=pl-s1>str</span>,<span class=pl-s1>opt</span>.<span class=pl-s1>year</span>.<span class=pl-en>strip</span>(<span class=pl-s>&#39;[]&#39;</span>).<span class=pl-en>split</span>(<span class=pl-s>&#39;,&#39;</span>))</td>
      </tr>
      <tr>
        <td id="L474" class="blob-num js-line-number" data-line-number="474"></td>
        <td id="LC474" class="blob-code blob-code-inner js-file-line"><span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L475" class="blob-num js-line-number" data-line-number="475"></td>
        <td id="LC475" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>years</span> <span class=pl-c1>=</span> [<span class=pl-s>&#39;2016&#39;</span>,<span class=pl-s>&#39;2017&#39;</span>,<span class=pl-s>&#39;2018&#39;</span>]</td>
      </tr>
      <tr>
        <td id="L476" class="blob-num js-line-number" data-line-number="476"></td>
        <td id="LC476" class="blob-code blob-code-inner js-file-line"><span class=pl-en>print</span>(<span class=pl-s1>years</span>)</td>
      </tr>
      <tr>
        <td id="L477" class="blob-num js-line-number" data-line-number="477"></td>
        <td id="LC477" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L478" class="blob-num js-line-number" data-line-number="478"></td>
        <td id="LC478" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>leptons</span> <span class=pl-c1>=</span> <span class=pl-en>map</span>(<span class=pl-s1>str</span>,<span class=pl-s1>opt</span>.<span class=pl-s1>lep</span>.<span class=pl-en>split</span>(<span class=pl-s>&#39;,&#39;</span>)) </td>
      </tr>
      <tr>
        <td id="L479" class="blob-num js-line-number" data-line-number="479"></td>
        <td id="LC479" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L480" class="blob-num js-line-number" data-line-number="480"></td>
        <td id="LC480" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>cut</span> <span class=pl-c1>=</span> <span class=pl-s1>opt</span>.<span class=pl-s1>cut</span> <span class=pl-c>#default cut must be obvious, for example lepton_eta&gt;-10.</span></td>
      </tr>
      <tr>
        <td id="L481" class="blob-num js-line-number" data-line-number="481"></td>
        <td id="LC481" class="blob-code blob-code-inner js-file-line"><span class=pl-k>if</span> <span class=pl-s1>opt</span>.<span class=pl-s1>cut</span> <span class=pl-c1>==</span> <span class=pl-s>&quot;lepton_eta&gt;-10.&quot;</span> <span class=pl-c1>and</span> <span class=pl-c1>not</span> <span class=pl-s1>opt</span>.<span class=pl-s1>sel</span>:</td>
      </tr>
      <tr>
        <td id="L482" class="blob-num js-line-number" data-line-number="482"></td>
        <td id="LC482" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>cut_dict</span> <span class=pl-c1>=</span> {<span class=pl-s>&#39;muon&#39;</span>:<span class=pl-s>&quot;lepton_eta&gt;-10&quot;</span>,<span class=pl-c>#&amp;&amp;best_topjet_isbtag==0&amp;&amp;best_Wpjet_isbtag==1&amp;&amp;nbjet_pt100==1&quot;, </span></td>
      </tr>
      <tr>
        <td id="L483" class="blob-num js-line-number" data-line-number="483"></td>
        <td id="LC483" class="blob-code blob-code-inner js-file-line">                 <span class=pl-s>&#39;electron&#39;</span>:<span class=pl-s>&quot;lepton_eta&gt;-10&quot;</span><span class=pl-c>#&amp;&amp;best_topjet_isbtag==0&amp;&amp;best_Wpjet_isbtag==1&amp;&amp;nbjet_pt100==1&quot;,</span></td>
      </tr>
      <tr>
        <td id="L484" class="blob-num js-line-number" data-line-number="484"></td>
        <td id="LC484" class="blob-code blob-code-inner js-file-line">     }</td>
      </tr>
      <tr>
        <td id="L485" class="blob-num js-line-number" data-line-number="485"></td>
        <td id="LC485" class="blob-code blob-code-inner js-file-line">     <span class=pl-s1>cut_tag</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;&quot;</span></td>
      </tr>
      <tr>
        <td id="L486" class="blob-num js-line-number" data-line-number="486"></td>
        <td id="LC486" class="blob-code blob-code-inner js-file-line"><span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L487" class="blob-num js-line-number" data-line-number="487"></td>
        <td id="LC487" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>if</span> <span class=pl-s1>opt</span>.<span class=pl-s1>sel</span>:</td>
      </tr>
      <tr>
        <td id="L488" class="blob-num js-line-number" data-line-number="488"></td>
        <td id="LC488" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>cut_dict</span> <span class=pl-c1>=</span> {<span class=pl-s>&#39;muon&#39;</span>:<span class=pl-s>&quot;MET_pt&gt;120&amp;&amp;lepton_pt&gt;50&amp;&amp;leadingjet_pt&gt;300&amp;&amp;subleadingjet_pt&gt;150&amp;&amp;&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>cut</span>, </td>
      </tr>
      <tr>
        <td id="L489" class="blob-num js-line-number" data-line-number="489"></td>
        <td id="LC489" class="blob-code blob-code-inner js-file-line">                      <span class=pl-s>&#39;electron&#39;</span>:<span class=pl-s>&quot;MET_pt&gt;120&amp;&amp;lepton_pt&gt;50&amp;&amp;leadingjet_pt&gt;300&amp;&amp;subleadingjet_pt&gt;150&amp;&amp;&quot;</span> <span class=pl-c1>+</span> <span class=pl-s1>cut</span></td>
      </tr>
      <tr>
        <td id="L490" class="blob-num js-line-number" data-line-number="490"></td>
        <td id="LC490" class="blob-code blob-code-inner js-file-line">          }</td>
      </tr>
      <tr>
        <td id="L491" class="blob-num js-line-number" data-line-number="491"></td>
        <td id="LC491" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span> <span class=pl-s1>opt</span>.<span class=pl-s1>cut</span> <span class=pl-c1>!=</span> <span class=pl-s>&quot;lepton_eta&gt;-10.&quot;</span>:</td>
      </tr>
      <tr>
        <td id="L492" class="blob-num js-line-number" data-line-number="492"></td>
        <td id="LC492" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>cut_tag</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;selection_AND_&#39;</span> <span class=pl-c1>+</span> <span class=pl-en>cutToTag</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>cut</span>) </td>
      </tr>
      <tr>
        <td id="L493" class="blob-num js-line-number" data-line-number="493"></td>
        <td id="LC493" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L494" class="blob-num js-line-number" data-line-number="494"></td>
        <td id="LC494" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>cut_tag</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;selection&#39;</span> </td>
      </tr>
      <tr>
        <td id="L495" class="blob-num js-line-number" data-line-number="495"></td>
        <td id="LC495" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>else</span>:</td>
      </tr>
      <tr>
        <td id="L496" class="blob-num js-line-number" data-line-number="496"></td>
        <td id="LC496" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>cut_dict</span> <span class=pl-c1>=</span> {<span class=pl-s>&#39;muon&#39;</span>:<span class=pl-s1>cut</span>, <span class=pl-s>&#39;electron&#39;</span>:<span class=pl-s1>cut</span>}</td>
      </tr>
      <tr>
        <td id="L497" class="blob-num js-line-number" data-line-number="497"></td>
        <td id="LC497" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>cut_tag</span> <span class=pl-c1>=</span> <span class=pl-en>cutToTag</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>cut</span>)</td>
      </tr>
      <tr>
        <td id="L498" class="blob-num js-line-number" data-line-number="498"></td>
        <td id="LC498" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L499" class="blob-num js-line-number" data-line-number="499"></td>
        <td id="LC499" class="blob-code blob-code-inner js-file-line"><span class=pl-s1>lumi</span> <span class=pl-c1>=</span> {<span class=pl-s>&#39;2016&#39;</span>: <span class=pl-c1>35.9</span>, <span class=pl-s>&quot;2017&quot;</span>: <span class=pl-c1>41.53</span>, <span class=pl-s>&quot;2018&quot;</span>: <span class=pl-c1>59.7</span>}</td>
      </tr>
      <tr>
        <td id="L500" class="blob-num js-line-number" data-line-number="500"></td>
        <td id="LC500" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L501" class="blob-num js-line-number" data-line-number="501"></td>
        <td id="LC501" class="blob-code blob-code-inner js-file-line"><span class=pl-k>for</span> <span class=pl-s1>year</span> <span class=pl-c1>in</span> <span class=pl-s1>years</span>:</td>
      </tr>
      <tr>
        <td id="L502" class="blob-num js-line-number" data-line-number="502"></td>
        <td id="LC502" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>sample</span> <span class=pl-c1>in</span> <span class=pl-s1>dataset_dict</span>[<span class=pl-s1>year</span>]:</td>
      </tr>
      <tr>
        <td id="L503" class="blob-num js-line-number" data-line-number="503"></td>
        <td id="LC503" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>merpart</span>):</td>
      </tr>
      <tr>
        <td id="L504" class="blob-num js-line-number" data-line-number="504"></td>
        <td id="LC504" class="blob-code blob-code-inner js-file-line">               <span class=pl-en>mergepart</span>(<span class=pl-s1>sample</span>)</td>
      </tr>
      <tr>
        <td id="L505" class="blob-num js-line-number" data-line-number="505"></td>
        <td id="LC505" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>lumi</span>):</td>
      </tr>
      <tr>
        <td id="L506" class="blob-num js-line-number" data-line-number="506"></td>
        <td id="LC506" class="blob-code blob-code-inner js-file-line">               <span class=pl-en>lumi_writer</span>(<span class=pl-s1>sample</span>, <span class=pl-s1>lumi</span>[<span class=pl-s1>year</span>])</td>
      </tr>
      <tr>
        <td id="L507" class="blob-num js-line-number" data-line-number="507"></td>
        <td id="LC507" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>mertree</span>):</td>
      </tr>
      <tr>
        <td id="L508" class="blob-num js-line-number" data-line-number="508"></td>
        <td id="LC508" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>if</span> <span class=pl-c1>not</span>(<span class=pl-s>&#39;WP&#39;</span> <span class=pl-c1>in</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span>):</td>
      </tr>
      <tr>
        <td id="L509" class="blob-num js-line-number" data-line-number="509"></td>
        <td id="LC509" class="blob-code blob-code-inner js-file-line">                    <span class=pl-en>mergetree</span>(<span class=pl-s1>sample</span>)</td>
      </tr>
      <tr>
        <td id="L510" class="blob-num js-line-number" data-line-number="510"></td>
        <td id="LC510" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L511" class="blob-num js-line-number" data-line-number="511"></td>
        <td id="LC511" class="blob-code blob-code-inner js-file-line"><span class=pl-k>for</span> <span class=pl-s1>year</span> <span class=pl-c1>in</span> <span class=pl-s1>years</span>:</td>
      </tr>
      <tr>
        <td id="L512" class="blob-num js-line-number" data-line-number="512"></td>
        <td id="LC512" class="blob-code blob-code-inner js-file-line">     <span class=pl-k>for</span> <span class=pl-s1>lep</span> <span class=pl-c1>in</span> <span class=pl-s1>leptons</span>:</td>
      </tr>
      <tr>
        <td id="L513" class="blob-num js-line-number" data-line-number="513"></td>
        <td id="LC513" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>dataset_new</span> <span class=pl-c1>=</span> <span class=pl-s1>dataset_dict</span>[<span class=pl-s1>year</span>]</td>
      </tr>
      <tr>
        <td id="L514" class="blob-num js-line-number" data-line-number="514"></td>
        <td id="LC514" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span> <span class=pl-s1>lep</span> <span class=pl-c1>==</span> <span class=pl-s>&#39;muon&#39;</span> <span class=pl-c1>and</span> <span class=pl-s1>sample_dict</span>[<span class=pl-s>&#39;DataEle_&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>year</span>)] <span class=pl-c1>in</span> <span class=pl-s1>dataset_new</span>:</td>
      </tr>
      <tr>
        <td id="L515" class="blob-num js-line-number" data-line-number="515"></td>
        <td id="LC515" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>dataset_new</span>.<span class=pl-en>remove</span>(<span class=pl-s1>sample_dict</span>[<span class=pl-s>&#39;DataEle_&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>year</span>)])</td>
      </tr>
      <tr>
        <td id="L516" class="blob-num js-line-number" data-line-number="516"></td>
        <td id="LC516" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>elif</span> <span class=pl-s1>lep</span> <span class=pl-c1>==</span> <span class=pl-s>&#39;electron&#39;</span> <span class=pl-c1>and</span> <span class=pl-s1>sample_dict</span>[<span class=pl-s>&#39;DataMu_&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>year</span>)] <span class=pl-c1>in</span> <span class=pl-s1>dataset_new</span>:</td>
      </tr>
      <tr>
        <td id="L517" class="blob-num js-line-number" data-line-number="517"></td>
        <td id="LC517" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>dataset_new</span>.<span class=pl-en>remove</span>(<span class=pl-s1>sample_dict</span>[<span class=pl-s>&#39;DataMu_&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>year</span>)])</td>
      </tr>
      <tr>
        <td id="L518" class="blob-num js-line-number" data-line-number="518"></td>
        <td id="LC518" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L519" class="blob-num js-line-number" data-line-number="519"></td>
        <td id="LC519" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span> <span class=pl-c1>=</span> []</td>
      </tr>
      <tr>
        <td id="L520" class="blob-num js-line-number" data-line-number="520"></td>
        <td id="LC520" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>wzero</span> <span class=pl-c1>=</span> <span class=pl-s>&#39;w_nominal&#39;</span></td>
      </tr>
      <tr>
        <td id="L521" class="blob-num js-line-number" data-line-number="521"></td>
        <td id="LC521" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>cut</span> <span class=pl-c1>=</span> <span class=pl-s1>cut_dict</span>[<span class=pl-s1>lep</span>]</td>
      </tr>
      <tr>
        <td id="L522" class="blob-num js-line-number" data-line-number="522"></td>
        <td id="LC522" class="blob-code blob-code-inner js-file-line">                    </td>
      </tr>
      <tr>
        <td id="L523" class="blob-num js-line-number" data-line-number="523"></td>
        <td id="LC523" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;lepton_pt&#39;</span>, <span class=pl-s>&#39;lepton p_{T} [GeV]&#39;</span>, <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>100</span>, <span class=pl-c1>0</span>, <span class=pl-c1>1200</span>))</td>
      </tr>
      <tr>
        <td id="L524" class="blob-num js-line-number" data-line-number="524"></td>
        <td id="LC524" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;lepton_eta&#39;</span>, <span class=pl-s>&#39;lepton #eta&#39;</span>, <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>48</span>, <span class=pl-c1>-</span><span class=pl-c1>2.4</span>, <span class=pl-c1>2.4</span>))</td>
      </tr>
      <tr>
        <td id="L525" class="blob-num js-line-number" data-line-number="525"></td>
        <td id="LC525" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;lepton_phi&#39;</span>, <span class=pl-s>&#39;lepton #phi&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>20</span>, <span class=pl-c1>-</span><span class=pl-c1>3.14</span>, <span class=pl-c1>3.14</span>))</td>
      </tr>
      <tr>
        <td id="L526" class="blob-num js-line-number" data-line-number="526"></td>
        <td id="LC526" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;lepton_miniIso&#39;</span>, <span class=pl-s>&#39;lepton miniIso&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>100</span>, <span class=pl-c1>0</span>, <span class=pl-c1>0.1</span>))</td>
      </tr>
      <tr>
        <td id="L527" class="blob-num js-line-number" data-line-number="527"></td>
        <td id="LC527" class="blob-code blob-code-inner js-file-line">          <span class=pl-c>#variables.append(variabile(&#39;lepton_stdIso&#39;, &#39;lepton std Iso&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 5, -0.5, 4.5))</span></td>
      </tr>
      <tr>
        <td id="L528" class="blob-num js-line-number" data-line-number="528"></td>
        <td id="LC528" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;best_top_m&#39;</span>, <span class=pl-s>&#39;top mass [GeV] (best)&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(best_top_m&gt;0&amp;&amp;&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>46</span>, <span class=pl-c1>80</span>, <span class=pl-c1>1000</span>))</td>
      </tr>
      <tr>
        <td id="L529" class="blob-num js-line-number" data-line-number="529"></td>
        <td id="LC529" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;MET_pt&#39;</span>, <span class=pl-s>&quot;Missing transverse momentum [GeV]&quot;</span>,<span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>100</span>, <span class=pl-c1>0</span>, <span class=pl-c1>1000</span>))</td>
      </tr>
      <tr>
        <td id="L530" class="blob-num js-line-number" data-line-number="530"></td>
        <td id="LC530" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;Event_HT&#39;</span>, <span class=pl-s>&#39;event HT [GeV]&#39;</span>, <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>70</span>, <span class=pl-c1>0</span>, <span class=pl-c1>1400</span>))</td>
      </tr>
      <tr>
        <td id="L531" class="blob-num js-line-number" data-line-number="531"></td>
        <td id="LC531" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;MET_phi&#39;</span>, <span class=pl-s>&#39;Missing transverse momentum #phi&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>20</span>, <span class=pl-c1>-</span><span class=pl-c1>3.14</span>, <span class=pl-c1>3.14</span>))</td>
      </tr>
      <tr>
        <td id="L532" class="blob-num js-line-number" data-line-number="532"></td>
        <td id="LC532" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;njet_lowpt&#39;</span>, <span class=pl-s>&#39;no. of jets with 25 &lt; p_{T} &lt; 100 GeV&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>8</span>, <span class=pl-c1>1.5</span>, <span class=pl-c1>9.5</span>))</td>
      </tr>
      <tr>
        <td id="L533" class="blob-num js-line-number" data-line-number="533"></td>
        <td id="LC533" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;njet_pt100&#39;</span>, <span class=pl-s>&#39;no. of jets with p_{T} &gt; 100 GeV&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>8</span>, <span class=pl-c1>1.5</span>, <span class=pl-c1>9.5</span>))</td>
      </tr>
      <tr>
        <td id="L534" class="blob-num js-line-number" data-line-number="534"></td>
        <td id="LC534" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;nbjet_lowpt&#39;</span>, <span class=pl-s>&#39;no. of b jets with 25 &lt; p_{T} &lt; 100 GeV&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>9</span>, <span class=pl-c1>-</span><span class=pl-c1>0.5</span>, <span class=pl-c1>8.5</span>))</td>
      </tr>
      <tr>
        <td id="L535" class="blob-num js-line-number" data-line-number="535"></td>
        <td id="LC535" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;nbjet_pt100&#39;</span>, <span class=pl-s>&#39;no. of b jets with p_{T} &gt; 100 GeV&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>7</span>, <span class=pl-c1>-</span><span class=pl-c1>0.5</span>, <span class=pl-c1>6.5</span>))</td>
      </tr>
      <tr>
        <td id="L536" class="blob-num js-line-number" data-line-number="536"></td>
        <td id="LC536" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;mtw&#39;</span>, <span class=pl-s>&#39;W boson transverse mass [GeV]&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>100</span>, <span class=pl-c1>0</span>, <span class=pl-c1>500</span>))</td>
      </tr>
      <tr>
        <td id="L537" class="blob-num js-line-number" data-line-number="537"></td>
        <td id="LC537" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;best_top_m&#39;</span>, <span class=pl-s>&#39;top mass [GeV] (best)&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(best_top_m&gt;0&amp;&amp;&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>,  <span class=pl-c1>46</span>, <span class=pl-c1>80</span>, <span class=pl-c1>1000</span>))</td>
      </tr>
      <tr>
        <td id="L538" class="blob-num js-line-number" data-line-number="538"></td>
        <td id="LC538" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;best_Wprime_m&#39;</span>, <span class=pl-s>&#39;Wprime mass [GeV] (best)&#39;</span>,  <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(best_Wprime_m&gt;0&amp;&amp;&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>,  <span class=pl-c1>61</span>, <span class=pl-c1>80</span>, <span class=pl-c1>5000</span>))</td>
      </tr>
      <tr>
        <td id="L539" class="blob-num js-line-number" data-line-number="539"></td>
        <td id="LC539" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;WprAK8_ttagMD&#39;</span>, <span class=pl-s>&#39;WprAK8 t tag MD&#39;</span>, <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(WprAK8_ttagMD&gt;-1&amp;&amp;&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>20</span>, <span class=pl-c1>0</span>, <span class=pl-c1>1.0</span>))</td>
      </tr>
      <tr>
        <td id="L540" class="blob-num js-line-number" data-line-number="540"></td>
        <td id="LC540" class="blob-code blob-code-inner js-file-line">          <span class=pl-s1>variables</span>.<span class=pl-en>append</span>(<span class=pl-en>variabile</span>(<span class=pl-s>&#39;WprAK8_tau2&#39;</span>, <span class=pl-s>&#39;WprAK8 tau 2&#39;</span>, <span class=pl-s1>wzero</span><span class=pl-c1>+</span><span class=pl-s>&#39;*(&#39;</span><span class=pl-c1>+</span><span class=pl-s1>cut</span><span class=pl-c1>+</span><span class=pl-s>&#39;)&#39;</span>, <span class=pl-c1>20</span>, <span class=pl-c1>0</span>, <span class=pl-c1>.4</span>))</td>
      </tr>
      <tr>
        <td id="L541" class="blob-num js-line-number" data-line-number="541"></td>
        <td id="LC541" class="blob-code blob-code-inner js-file-line">          <span class=pl-s>&#39;&#39;&#39;</span></td>
      </tr>
      <tr>
        <td id="L542" class="blob-num js-line-number" data-line-number="542"></td>
        <td id="LC542" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_topjet_isbtag&#39;, &#39;top jet b tagged (best)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 2, -0.5, 1.5))</span></td>
      </tr>
      <tr>
        <td id="L543" class="blob-num js-line-number" data-line-number="543"></td>
        <td id="LC543" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_Wpjet_isbtag&#39;, &quot;W&#39; jet b tagged (best)&quot;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 2, -0.5, 1.5))</span></td>
      </tr>
      <tr>
        <td id="L544" class="blob-num js-line-number" data-line-number="544"></td>
        <td id="LC544" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;MC_Wpjet_pt&#39;, &quot;MCtruth W&#39; jet p_{T} [GeV]&quot;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L545" class="blob-num js-line-number" data-line-number="545"></td>
        <td id="LC545" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;MC_topjet_pt&#39;, &quot;MCtruth top jet p_{T} [GeV]&quot;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L546" class="blob-num js-line-number" data-line-number="546"></td>
        <td id="LC546" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;MC_top_pt&#39;, &quot;MCtruth top p_{T} [GeV]&quot;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L547" class="blob-num js-line-number" data-line-number="547"></td>
        <td id="LC547" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;MC_top_m&#39;, &quot;MCtruth top m [GeV]&quot;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 46, 80, 1000))</span></td>
      </tr>
      <tr>
        <td id="L548" class="blob-num js-line-number" data-line-number="548"></td>
        <td id="LC548" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;MC_Wprime_pt&#39;, &#39;Wprime p_{T} [GeV] (MC)&#39;,  wzero+&#39;*(MC_Wprime_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L549" class="blob-num js-line-number" data-line-number="549"></td>
        <td id="LC549" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;MC_Wprime_eta&#39;, &#39;Wprime #eta (MC)&#39;, wzero+&#39;*(MC_Wprime_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L550" class="blob-num js-line-number" data-line-number="550"></td>
        <td id="LC550" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;MC_Wprime_phi&#39;, &#39;Wprime #phi (MC)&#39;,  wzero+&#39;*(MC_Wprime_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L551" class="blob-num js-line-number" data-line-number="551"></td>
        <td id="LC551" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;MC_Wprime_m&#39;, &#39;Wprime mass [GeV] (MC)&#39;,  wzero+&#39;*(MC_Wprime_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;,  61, 80, 5000))</span></td>
      </tr>
      <tr>
        <td id="L552" class="blob-num js-line-number" data-line-number="552"></td>
        <td id="LC552" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          </span></td>
      </tr>
      <tr>
        <td id="L553" class="blob-num js-line-number" data-line-number="553"></td>
        <td id="LC553" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;bjets_pt&#39;, &#39;leading bjets system p_{T} [GeV]&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L554" class="blob-num js-line-number" data-line-number="554"></td>
        <td id="LC554" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;leadingbjet_pt&#39;, &#39;leading bjet p_{T} [GeV]&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L555" class="blob-num js-line-number" data-line-number="555"></td>
        <td id="LC555" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;subleadingbjet_pt&#39;, &#39;subleading bjet p_{T} [GeV]&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))          </span></td>
      </tr>
      <tr>
        <td id="L556" class="blob-num js-line-number" data-line-number="556"></td>
        <td id="LC556" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;nfatjet&#39;, &#39;no. of AK8 jets&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 5, 1.5, 6.5))</span></td>
      </tr>
      <tr>
        <td id="L557" class="blob-num js-line-number" data-line-number="557"></td>
        <td id="LC557" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;lepMET_deltaphi&#39;, &#39;#Delta#phi(l, MET)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L558" class="blob-num js-line-number" data-line-number="558"></td>
        <td id="LC558" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_area&#39;, &#39;topAK8 area&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 30, 1.5, 3.0))</span></td>
      </tr>
      <tr>
        <td id="L559" class="blob-num js-line-number" data-line-number="559"></td>
        <td id="LC559" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_btag&#39;, &#39;topAK8 b tag &#39;, wzero+&#39;*(topAK8_btag&gt;-1&amp;&amp;&#39;+cut+&#39;)&#39;, 20, 0, 1.0))</span></td>
      </tr>
      <tr>
        <td id="L560" class="blob-num js-line-number" data-line-number="560"></td>
        <td id="LC560" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_ttagMD&#39;, &#39;topAK8 t tag MD&#39;, wzero+&#39;*(topAK8_ttagMD&gt;-1&amp;&amp;&#39;+cut+&#39;)&#39;, 20, 0, 1.0))</span></td>
      </tr>
      <tr>
        <td id="L561" class="blob-num js-line-number" data-line-number="561"></td>
        <td id="LC561" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_ttag&#39;, &#39;topAK8 t tag&#39;, wzero+&#39;*(topAK8_ttag&gt;-1&amp;&amp;&#39;+cut+&#39;)&#39;, 20, 0, 1.0))</span></td>
      </tr>
      <tr>
        <td id="L562" class="blob-num js-line-number" data-line-number="562"></td>
        <td id="LC562" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_eta&#39;, &#39;topAK8 #eta&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 48, -4.8, 4.8)) </span></td>
      </tr>
      <tr>
        <td id="L563" class="blob-num js-line-number" data-line-number="563"></td>
        <td id="LC563" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_m&#39;, &#39;topAK8 mass [GeV]&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 40, 0, 400))</span></td>
      </tr>
      <tr>
        <td id="L564" class="blob-num js-line-number" data-line-number="564"></td>
        <td id="LC564" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_mSD&#39;, &#39;topAK8 soft drop mass [GeV]&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 40, 0, 400))</span></td>
      </tr>
      <tr>
        <td id="L565" class="blob-num js-line-number" data-line-number="565"></td>
        <td id="LC565" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_phi&#39;, &#39;topAK8 #phi&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L566" class="blob-num js-line-number" data-line-number="566"></td>
        <td id="LC566" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_pt&#39;, &#39;topAK8 p_{T} [GeV]&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 200, 0, 2000))</span></td>
      </tr>
      <tr>
        <td id="L567" class="blob-num js-line-number" data-line-number="567"></td>
        <td id="LC567" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_tau1&#39;, &#39;topAK8 tau 1&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 80, 0, .8))</span></td>
      </tr>
      <tr>
        <td id="L568" class="blob-num js-line-number" data-line-number="568"></td>
        <td id="LC568" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_tau2&#39;, &#39;topAK8 tau 2&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 60, 0, .6))</span></td>
      </tr>
      <tr>
        <td id="L569" class="blob-num js-line-number" data-line-number="569"></td>
        <td id="LC569" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_tau3&#39;, &#39;topAK8 tau 3&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 40, 0, .4))</span></td>
      </tr>
      <tr>
        <td id="L570" class="blob-num js-line-number" data-line-number="570"></td>
        <td id="LC570" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;topAK8_tau4&#39;, &#39;topAK8 tau 4&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, 0, .2))</span></td>
      </tr>
      <tr>
        <td id="L571" class="blob-num js-line-number" data-line-number="571"></td>
        <td id="LC571" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          </span></td>
      </tr>
      <tr>
        <td id="L572" class="blob-num js-line-number" data-line-number="572"></td>
        <td id="LC572" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_lep_closestjet&#39;, &#39;#DeltaR lep closest jet&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L573" class="blob-num js-line-number" data-line-number="573"></td>
        <td id="LC573" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_lep_leadingjet&#39;, &#39;#DeltaR lep lead jet&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L574" class="blob-num js-line-number" data-line-number="574"></td>
        <td id="LC574" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_lep_subleadingjet&#39;, &#39;#DeltaR lep sub-lead jet&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L575" class="blob-num js-line-number" data-line-number="575"></td>
        <td id="LC575" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_top_pt&#39;, &#39;top p_{T} [GeV] (best)&#39;,  wzero+&#39;*(best_top_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L576" class="blob-num js-line-number" data-line-number="576"></td>
        <td id="LC576" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_top_eta&#39;, &#39;top #eta (best)&#39;, wzero+&#39;*(best_top_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L577" class="blob-num js-line-number" data-line-number="577"></td>
        <td id="LC577" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_top_phi&#39;, &#39;top #phi (best)&#39;,  wzero+&#39;*(best_top_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L578" class="blob-num js-line-number" data-line-number="578"></td>
        <td id="LC578" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_top_pt&#39;, &#39;top p_{T} [GeV] (chimass)&#39;,  wzero+&#39;*(chi_top_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L579" class="blob-num js-line-number" data-line-number="579"></td>
        <td id="LC579" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_top_eta&#39;, &#39;top #eta (chimass)&#39;, wzero+&#39;*(chi_top_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L580" class="blob-num js-line-number" data-line-number="580"></td>
        <td id="LC580" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_top_phi&#39;, &#39;top #phi (chimass)&#39;,  wzero+&#39;*(chi_top_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L581" class="blob-num js-line-number" data-line-number="581"></td>
        <td id="LC581" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_top_m&#39;, &#39;top mass [GeV] (chimass)&#39;,  wzero+&#39;*(chi_top_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;,  46, 80, 1000))</span></td>
      </tr>
      <tr>
        <td id="L582" class="blob-num js-line-number" data-line-number="582"></td>
        <td id="LC582" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_top_pt&#39;, &#39;top p_{T} [GeV] (closest)&#39;,  wzero+&#39;*(closest_top_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L583" class="blob-num js-line-number" data-line-number="583"></td>
        <td id="LC583" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_top_eta&#39;, &#39;top #eta (closest)&#39;, wzero+&#39;*(closest_top_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L584" class="blob-num js-line-number" data-line-number="584"></td>
        <td id="LC584" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_top_phi&#39;, &#39;top #phi (closest)&#39;,  wzero+&#39;*(closest_top_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L585" class="blob-num js-line-number" data-line-number="585"></td>
        <td id="LC585" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_top_m&#39;, &#39;top mass [GeV] (closest)&#39;,  wzero+&#39;*(closest_top_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 46, 80, 1000))</span></td>
      </tr>
      <tr>
        <td id="L586" class="blob-num js-line-number" data-line-number="586"></td>
        <td id="LC586" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_top_pt&#39;, &#39;top p_{T} [GeV] (sublead)&#39;,  wzero+&#39;*(sublead_top_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L587" class="blob-num js-line-number" data-line-number="587"></td>
        <td id="LC587" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_top_eta&#39;, &#39;top #eta (sublead)&#39;, wzero+&#39;*(sublead_top_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L588" class="blob-num js-line-number" data-line-number="588"></td>
        <td id="LC588" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_top_phi&#39;, &#39;top #phi (sublead)&#39;,  wzero+&#39;*(sublead_top_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L589" class="blob-num js-line-number" data-line-number="589"></td>
        <td id="LC589" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_top_m&#39;, &#39;top mass [GeV] (sublead)&#39;,  wzero+&#39;*(sublead_top_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 46, 80, 1000))</span></td>
      </tr>
      <tr>
        <td id="L590" class="blob-num js-line-number" data-line-number="590"></td>
        <td id="LC590" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_top_pt&#39;, &#39;top p_{T} [GeV] (GenPart)&#39;,  wzero+&#39;*(GenPart_top_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L591" class="blob-num js-line-number" data-line-number="591"></td>
        <td id="LC591" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_top_eta&#39;, &#39;top #eta (GenPart)&#39;, wzero+&#39;*(GenPart_top_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L592" class="blob-num js-line-number" data-line-number="592"></td>
        <td id="LC592" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_top_phi&#39;, &#39;top #phi (GenPart)&#39;,  wzero+&#39;*(GenPart_top_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L593" class="blob-num js-line-number" data-line-number="593"></td>
        <td id="LC593" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_top_m&#39;, &#39;top mass [GeV] (GenPart)&#39;,  wzero+&#39;*(GenPart_top_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 46, 80, 1000))</span></td>
      </tr>
      <tr>
        <td id="L594" class="blob-num js-line-number" data-line-number="594"></td>
        <td id="LC594" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_bottom_pt&#39;, &#39;bottom p_{T} [GeV] (GenPart)&#39;,  wzero+&#39;*(GenPart_bottom_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L595" class="blob-num js-line-number" data-line-number="595"></td>
        <td id="LC595" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_bottom_eta&#39;, &#39;bottom #eta (GenPart)&#39;, wzero+&#39;*(GenPart_bottom_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L596" class="blob-num js-line-number" data-line-number="596"></td>
        <td id="LC596" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_bottom_phi&#39;, &#39;bottom #phi (GenPart)&#39;,  wzero+&#39;*(GenPart_bottom_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L597" class="blob-num js-line-number" data-line-number="597"></td>
        <td id="LC597" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_bottom_m&#39;, &#39;bottom mass [GeV] (GenPart)&#39;,  wzero+&#39;*(GenPart_bottom_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;,  92, 80, 1000))</span></td>
      </tr>
      <tr>
        <td id="L598" class="blob-num js-line-number" data-line-number="598"></td>
        <td id="LC598" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_Wprime_pt&#39;, &#39;Wprime p_{T} [GeV] (chimass)&#39;,  wzero+&#39;*(chi_Wprime_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L599" class="blob-num js-line-number" data-line-number="599"></td>
        <td id="LC599" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_Wprime_eta&#39;, &#39;Wprime #eta (chimass)&#39;, wzero+&#39;*(chi_Wprime_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L600" class="blob-num js-line-number" data-line-number="600"></td>
        <td id="LC600" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_Wprime_phi&#39;, &#39;Wprime #phi (chimass)&#39;,  wzero+&#39;*(chi_Wprime_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L601" class="blob-num js-line-number" data-line-number="601"></td>
        <td id="LC601" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_Wprime_m&#39;, &#39;Wprime mass [GeV] (chimass)&#39;,  wzero+&#39;*(chi_Wprime_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;,  61, 80, 5000))</span></td>
      </tr>
      <tr>
        <td id="L602" class="blob-num js-line-number" data-line-number="602"></td>
        <td id="LC602" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_Wprime_pt&#39;, &#39;Wprime p_{T} [GeV] (best)&#39;,  wzero+&#39;*(best_Wprime_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L603" class="blob-num js-line-number" data-line-number="603"></td>
        <td id="LC603" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_Wprime_eta&#39;, &#39;Wprime #eta (best)&#39;, wzero+&#39;*(best_Wprime_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L604" class="blob-num js-line-number" data-line-number="604"></td>
        <td id="LC604" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_Wprime_phi&#39;, &#39;Wprime #phi (best)&#39;,  wzero+&#39;*(best_Wprime_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L605" class="blob-num js-line-number" data-line-number="605"></td>
        <td id="LC605" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_Wprime_pt&#39;, &#39;Wprime p_{T} [GeV] (closest)&#39;,  wzero+&#39;*(closest_Wprime_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L606" class="blob-num js-line-number" data-line-number="606"></td>
        <td id="LC606" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_Wprime_eta&#39;, &#39;Wprime #eta (closest)&#39;, wzero+&#39;*(closest_Wprime_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L607" class="blob-num js-line-number" data-line-number="607"></td>
        <td id="LC607" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_Wprime_phi&#39;, &#39;Wprime #phi (closest)&#39;,  wzero+&#39;*(closest_Wprime_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L608" class="blob-num js-line-number" data-line-number="608"></td>
        <td id="LC608" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_Wprime_m&#39;, &#39;Wprime mass [GeV] (closest)&#39;,  wzero+&#39;*(closest_Wprime_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;,  61, 80, 5000))</span></td>
      </tr>
      <tr>
        <td id="L609" class="blob-num js-line-number" data-line-number="609"></td>
        <td id="LC609" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_Wprime_pt&#39;, &#39;Wprime p_{T} [GeV] (sublead)&#39;,  wzero+&#39;*(sublead_Wprime_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L610" class="blob-num js-line-number" data-line-number="610"></td>
        <td id="LC610" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_Wprime_eta&#39;, &#39;Wprime #eta (sublead)&#39;, wzero+&#39;*(sublead_Wprime_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L611" class="blob-num js-line-number" data-line-number="611"></td>
        <td id="LC611" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_Wprime_phi&#39;, &#39;Wprime #phi (sublead)&#39;,  wzero+&#39;*(sublead_Wprime_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L612" class="blob-num js-line-number" data-line-number="612"></td>
        <td id="LC612" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_Wprime_m&#39;, &#39;Wprime mass [GeV] (sublead)&#39;,  wzero+&#39;*(sublead_Wprime_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;,  61, 80, 5000))</span></td>
      </tr>
      <tr>
        <td id="L613" class="blob-num js-line-number" data-line-number="613"></td>
        <td id="LC613" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_Wprime_pt&#39;, &#39;Wprime p_{T} [GeV] (GenPart)&#39;,  wzero+&#39;*(GenPart_Wprime_pt&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L614" class="blob-num js-line-number" data-line-number="614"></td>
        <td id="LC614" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_Wprime_eta&#39;, &#39;Wprime #eta (GenPart)&#39;, wzero+&#39;*(GenPart_Wprime_eta&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4., 4.))</span></td>
      </tr>
      <tr>
        <td id="L615" class="blob-num js-line-number" data-line-number="615"></td>
        <td id="LC615" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_Wprime_phi&#39;, &#39;Wprime #phi (GenPart)&#39;,  wzero+&#39;*(GenPart_Wprime_phi&gt;-4.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L616" class="blob-num js-line-number" data-line-number="616"></td>
        <td id="LC616" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;GenPart_Wprime_m&#39;, &#39;Wprime mass [GeV] (GenPart)&#39;,  wzero+&#39;*(GenPart_Wprime_m&gt;0&amp;&amp;&#39;+cut+&#39;)&#39;,  61, 80, 5000))</span></td>
      </tr>
      <tr>
        <td id="L617" class="blob-num js-line-number" data-line-number="617"></td>
        <td id="LC617" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_topjet_pt&#39;, &#39;sub leading jet p_{T} [GeV]&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L618" class="blob-num js-line-number" data-line-number="618"></td>
        <td id="LC618" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_topjet_eta&#39;, &#39;sub leading jet #eta&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 48, -2.4, 2.4))</span></td>
      </tr>
      <tr>
        <td id="L619" class="blob-num js-line-number" data-line-number="619"></td>
        <td id="LC619" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_topjet_eta&#39;, &#39;closest top jet #eta&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 48, -2.4, 2.4))</span></td>
      </tr>
      <tr>
        <td id="L620" class="blob-num js-line-number" data-line-number="620"></td>
        <td id="LC620" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_topjet_pt&#39;, &#39;closest top jet p_{T} [GeV]&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L621" class="blob-num js-line-number" data-line-number="621"></td>
        <td id="LC621" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_topjet_eta&#39;, &#39;chi top jet #eta&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 48, -2.4, 2.4))</span></td>
      </tr>
      <tr>
        <td id="L622" class="blob-num js-line-number" data-line-number="622"></td>
        <td id="LC622" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_topjet_pt&#39;, &#39;chi top jet p_{T} [GeV]&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L623" class="blob-num js-line-number" data-line-number="623"></td>
        <td id="LC623" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_topjet_eta&#39;, &#39;best top jet #eta&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 48, -2.4, 2.4))</span></td>
      </tr>
      <tr>
        <td id="L624" class="blob-num js-line-number" data-line-number="624"></td>
        <td id="LC624" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_topjet_pt&#39;, &#39;best top jet p_{T} [GeV]&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L625" class="blob-num js-line-number" data-line-number="625"></td>
        <td id="LC625" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_Wpjet_pt&#39;, &#39;(sublead) leading jet p_{T} [GeV] &#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L626" class="blob-num js-line-number" data-line-number="626"></td>
        <td id="LC626" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_Wpjet_pt&#39;, &#39;(closest) leading jet p_{T} [GeV] &#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L627" class="blob-num js-line-number" data-line-number="627"></td>
        <td id="LC627" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_Wpjet_pt&#39;, &#39;(best) leading jet p_{T} [GeV] &#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L628" class="blob-num js-line-number" data-line-number="628"></td>
        <td id="LC628" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_Wpjet_pt&#39;, &#39;(chimass) leading jet p_{T} [GeV] &#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L629" class="blob-num js-line-number" data-line-number="629"></td>
        <td id="LC629" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          </span></td>
      </tr>
      <tr>
        <td id="L630" class="blob-num js-line-number" data-line-number="630"></td>
        <td id="LC630" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_Wpjet_eta&#39;, &#39;leading jet #eta&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 48, -2.4, 2.4))</span></td>
      </tr>
      <tr>
        <td id="L631" class="blob-num js-line-number" data-line-number="631"></td>
        <td id="LC631" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_Wpjet_isbtag&#39;, &#39;leading jet b tagged&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 2, -0.5, 1.5))</span></td>
      </tr>
      <tr>
        <td id="L632" class="blob-num js-line-number" data-line-number="632"></td>
        <td id="LC632" class="blob-code blob-code-inner js-file-line"><span class=pl-s></span></td>
      </tr>
      <tr>
        <td id="L633" class="blob-num js-line-number" data-line-number="633"></td>
        <td id="LC633" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;leadingjets_deltaR&#39;, &#39;leadings jets #DeltaR&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 10, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L634" class="blob-num js-line-number" data-line-number="634"></td>
        <td id="LC634" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;leadingjets_deltaPhi&#39;, &#39;leadings jets #Delta#phi&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L635" class="blob-num js-line-number" data-line-number="635"></td>
        <td id="LC635" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;leadingjets_deltaEta&#39;, &#39;leadings jets #Delta#eta&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 48, -4.8, 4.8))</span></td>
      </tr>
      <tr>
        <td id="L636" class="blob-num js-line-number" data-line-number="636"></td>
        <td id="LC636" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;leadingjets_pt&#39;, &#39;leadings jets system p_{T} [GeV]&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L637" class="blob-num js-line-number" data-line-number="637"></td>
        <td id="LC637" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;bjets_deltaR&#39;, &#39;b jets #DeltaR&#39;,  wzero+&#39;*(bjets_deltaR&gt;-50.&amp;&amp;&#39;+cut+&#39;)&#39;, 10, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L638" class="blob-num js-line-number" data-line-number="638"></td>
        <td id="LC638" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;bjets_deltaPhi&#39;, &#39;b jets #Delta#phi&#39;,  wzero+&#39;*(bjets_deltaPhi&gt;-50.&amp;&amp;&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L639" class="blob-num js-line-number" data-line-number="639"></td>
        <td id="LC639" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;bjets_deltaEta&#39;, &#39;b jets #Delta#eta&#39;,  wzero+&#39;*(bjets_deltaEta&gt;-50.&amp;&amp;&#39;+cut+&#39;)&#39;, 48, -4.8, 4.8))</span></td>
      </tr>
      <tr>
        <td id="L640" class="blob-num js-line-number" data-line-number="640"></td>
        <td id="LC640" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;bjets_pt&#39;, &#39;b jets system p_{T} [GeV]&#39;,  wzero+&#39;*(bjets_pt&gt;-10.&amp;&amp;&#39;+cut+&#39;)&#39;, 150, 0, 3000))</span></td>
      </tr>
      <tr>
        <td id="L641" class="blob-num js-line-number" data-line-number="641"></td>
        <td id="LC641" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;had_global_thrust&#39;, &#39;hadronic global thrust&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, 0.5, 1))</span></td>
      </tr>
      <tr>
        <td id="L642" class="blob-num js-line-number" data-line-number="642"></td>
        <td id="LC642" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;had_central_thrust&#39;, &#39;hadronic transverse thrust&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, 0, 0.5))</span></td>
      </tr>
      <tr>
        <td id="L643" class="blob-num js-line-number" data-line-number="643"></td>
        <td id="LC643" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;ovr_global_thrust&#39;, &#39;event global thrust&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, 0.5, 1))</span></td>
      </tr>
      <tr>
        <td id="L644" class="blob-num js-line-number" data-line-number="644"></td>
        <td id="LC644" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;ovr_central_thrust&#39;, &#39;event transverse thrust&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, 0, 0.5))</span></td>
      </tr>
      <tr>
        <td id="L645" class="blob-num js-line-number" data-line-number="645"></td>
        <td id="LC645" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_topjet_dRLepJet&#39;, &#39;#DeltaR lep jet (best crit)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L646" class="blob-num js-line-number" data-line-number="646"></td>
        <td id="LC646" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;closest_topjet_dRLepJet&#39;, &#39;#DeltaR lep jet (closest crit)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L647" class="blob-num js-line-number" data-line-number="647"></td>
        <td id="LC647" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;sublead_topjet_dRLepJet&#39;, &#39;#DeltaR lep jet (sublead crit)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L648" class="blob-num js-line-number" data-line-number="648"></td>
        <td id="LC648" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_topjet_dRLepJet&#39;, &#39;#DeltaR lep jet (chi crit)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L649" class="blob-num js-line-number" data-line-number="649"></td>
        <td id="LC649" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;ptrel_leadAK4_closestAK8&#39;, &#39;pt rel leading AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L650" class="blob-num js-line-number" data-line-number="650"></td>
        <td id="LC650" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_leadAK4_closestAK8&#39;, &#39;#DeltaR leading AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;,  20, 0, 2))</span></td>
      </tr>
      <tr>
        <td id="L651" class="blob-num js-line-number" data-line-number="651"></td>
        <td id="LC651" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;ptrel_subleadAK4_closestAK8&#39;, &#39;pt rel sub-leading AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L652" class="blob-num js-line-number" data-line-number="652"></td>
        <td id="LC652" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_subleadAK4_closestAK8&#39;, &#39;#DeltaR sub-leading AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L653" class="blob-num js-line-number" data-line-number="653"></td>
        <td id="LC653" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;ptrel_besttopAK4_closestAK8&#39;, &#39;pt rel (best)top AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L654" class="blob-num js-line-number" data-line-number="654"></td>
        <td id="LC654" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_besttopAK4_closestAK8&#39;, &#39;#DeltaR (best)top AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L655" class="blob-num js-line-number" data-line-number="655"></td>
        <td id="LC655" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;ptrel_bestWAK4_closestAK8&#39;, &#39;pt rel (best)W<span class=pl-cce>\&#39;</span> AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L656" class="blob-num js-line-number" data-line-number="656"></td>
        <td id="LC656" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_bestWAK4_closestAK8&#39;, &#39;#DeltaR (best)W<span class=pl-cce>\&#39;</span> AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L657" class="blob-num js-line-number" data-line-number="657"></td>
        <td id="LC657" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_topW_jets_pt&#39;, &#39;jets (t+W<span class=pl-cce>\&#39;</span>) p_{T} [GeV] (best)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 1500))</span></td>
      </tr>
      <tr>
        <td id="L658" class="blob-num js-line-number" data-line-number="658"></td>
        <td id="LC658" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_topW_jets_deltaR&#39;, &#39;#DeltaR jets (t+W<span class=pl-cce>\&#39;</span>) (best)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L659" class="blob-num js-line-number" data-line-number="659"></td>
        <td id="LC659" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_topW_jets_deltaPhi&#39;, &#39;#Delta #phi jets (t+W<span class=pl-cce>\&#39;</span>) (best)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L660" class="blob-num js-line-number" data-line-number="660"></td>
        <td id="LC660" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;ptrel_chitopAK4_closestAK8&#39;, &#39;pt rel (chi)top AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L661" class="blob-num js-line-number" data-line-number="661"></td>
        <td id="LC661" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_chitopAK4_closestAK8&#39;, &#39;#DeltaR (chi)top AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L662" class="blob-num js-line-number" data-line-number="662"></td>
        <td id="LC662" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;ptrel_chiWAK4_closestAK8&#39;, &#39;pt rel (chi)W<span class=pl-cce>\&#39;</span> AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L663" class="blob-num js-line-number" data-line-number="663"></td>
        <td id="LC663" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;deltaR_chiWAK4_closestAK8&#39;, &#39;#DeltaR (chi)W<span class=pl-cce>\&#39;</span> AK4 closest AK8&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L664" class="blob-num js-line-number" data-line-number="664"></td>
        <td id="LC664" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_topW_jets_pt&#39;, &#39;jets (t+W<span class=pl-cce>\&#39;</span>) p_{T} [GeV] (chi)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 150, 0, 1500))</span></td>
      </tr>
      <tr>
        <td id="L665" class="blob-num js-line-number" data-line-number="665"></td>
        <td id="LC665" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_topW_jets_deltaR&#39;, &#39;#DeltaR jets (t+W<span class=pl-cce>\&#39;</span>) (chi)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 5))</span></td>
      </tr>
      <tr>
        <td id="L666" class="blob-num js-line-number" data-line-number="666"></td>
        <td id="LC666" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;chi_topW_jets_deltaPhi&#39;, &#39;#Delta #phi jets (t+W<span class=pl-cce>\&#39;</span>) (chi)&#39;,  wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L667" class="blob-num js-line-number" data-line-number="667"></td>
        <td id="LC667" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;nPV_good&#39;, &#39;n good PV&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 120, 0, 120))</span></td>
      </tr>
      <tr>
        <td id="L668" class="blob-num js-line-number" data-line-number="668"></td>
        <td id="LC668" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;nPV_tot&#39;, &#39;total n PV&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 120, 0, 120))</span></td>
      </tr>
      <tr>
        <td id="L669" class="blob-num js-line-number" data-line-number="669"></td>
        <td id="LC669" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          </span></td>
      </tr>
      <tr>
        <td id="L670" class="blob-num js-line-number" data-line-number="670"></td>
        <td id="LC670" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_top_costhetalep&#39;, &#39;cos #theta (lepton)&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 1))</span></td>
      </tr>
      <tr>
        <td id="L671" class="blob-num js-line-number" data-line-number="671"></td>
        <td id="LC671" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;best_top_costheta&#39;, &#39;cos #theta&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 50, 0, 1))</span></td>
      </tr>
      <tr>
        <td id="L672" class="blob-num js-line-number" data-line-number="672"></td>
        <td id="LC672" class="blob-code blob-code-inner js-file-line"><span class=pl-s></span></td>
      </tr>
      <tr>
        <td id="L673" class="blob-num js-line-number" data-line-number="673"></td>
        <td id="LC673" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_area&#39;,  &quot;W&#39; AK8 area&quot;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 30, 1.5, 3.0))</span></td>
      </tr>
      <tr>
        <td id="L674" class="blob-num js-line-number" data-line-number="674"></td>
        <td id="LC674" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_btag&#39;, &#39;WprAK8 b tag &#39;, wzero+&#39;*(WprAK8_btag&gt;-1&amp;&amp;&#39;+cut+&#39;)&#39;, 20, 0, 1.0))</span></td>
      </tr>
      <tr>
        <td id="L675" class="blob-num js-line-number" data-line-number="675"></td>
        <td id="LC675" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_ttagMD&#39;, &#39;WprAK8 t tag MD&#39;, wzero+&#39;*(WprAK8_ttagMD&gt;-1&amp;&amp;&#39;+cut+&#39;)&#39;, 20, 0, 1.0))</span></td>
      </tr>
      <tr>
        <td id="L676" class="blob-num js-line-number" data-line-number="676"></td>
        <td id="LC676" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_ttag&#39;, &#39;WprAK8 t tag&#39;, wzero+&#39;*(WprAK8_ttag&gt;-1&amp;&amp;&#39;+cut+&#39;)&#39;, 20, 0, 1.0))</span></td>
      </tr>
      <tr>
        <td id="L677" class="blob-num js-line-number" data-line-number="677"></td>
        <td id="LC677" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_eta&#39;, &#39;WprAK8 #eta&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 48, -4.8, 4.8)) </span></td>
      </tr>
      <tr>
        <td id="L678" class="blob-num js-line-number" data-line-number="678"></td>
        <td id="LC678" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_m&#39;, &#39;WprAK8 mass [GeV]&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 40, 0, 400))</span></td>
      </tr>
      <tr>
        <td id="L679" class="blob-num js-line-number" data-line-number="679"></td>
        <td id="LC679" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_mSD&#39;, &#39;WprAK8 soft drop mass [GeV]&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 40, 0, 400))</span></td>
      </tr>
      <tr>
        <td id="L680" class="blob-num js-line-number" data-line-number="680"></td>
        <td id="LC680" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_phi&#39;, &#39;WprAK8 #phi&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, -3.14, 3.14))</span></td>
      </tr>
      <tr>
        <td id="L681" class="blob-num js-line-number" data-line-number="681"></td>
        <td id="LC681" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_pt&#39;, &#39;WprAK8 p_{T} [GeV]&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 200, 0, 2000))</span></td>
      </tr>
      <tr>
        <td id="L682" class="blob-num js-line-number" data-line-number="682"></td>
        <td id="LC682" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_tau1&#39;, &#39;WprAK8 tau 1&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 80, 0, .8))</span></td>
      </tr>
      <tr>
        <td id="L683" class="blob-num js-line-number" data-line-number="683"></td>
        <td id="LC683" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_tau2&#39;, &#39;WprAK8 tau 2&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 60, 0, .6))</span></td>
      </tr>
      <tr>
        <td id="L684" class="blob-num js-line-number" data-line-number="684"></td>
        <td id="LC684" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_tau3&#39;, &#39;WprAK8 tau 3&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 40, 0, .4))</span></td>
      </tr>
      <tr>
        <td id="L685" class="blob-num js-line-number" data-line-number="685"></td>
        <td id="LC685" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          variables.append(variabile(&#39;WprAK8_tau4&#39;, &#39;WprAK8 tau 4&#39;, wzero+&#39;*(&#39;+cut+&#39;)&#39;, 20, 0, .2))</span></td>
      </tr>
      <tr>
        <td id="L686" class="blob-num js-line-number" data-line-number="686"></td>
        <td id="LC686" class="blob-code blob-code-inner js-file-line"><span class=pl-s>          &#39;&#39;&#39;</span></td>
      </tr>
      <tr>
        <td id="L687" class="blob-num js-line-number" data-line-number="687"></td>
        <td id="LC687" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>for</span> <span class=pl-s1>sample</span> <span class=pl-c1>in</span> <span class=pl-s1>dataset_new</span>:</td>
      </tr>
      <tr>
        <td id="L688" class="blob-num js-line-number" data-line-number="688"></td>
        <td id="LC688" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>if</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>plot</span>):</td>
      </tr>
      <tr>
        <td id="L689" class="blob-num js-line-number" data-line-number="689"></td>
        <td id="LC689" class="blob-code blob-code-inner js-file-line">                    <span class=pl-k>for</span> <span class=pl-s1>var</span> <span class=pl-c1>in</span> <span class=pl-s1>variables</span>:</td>
      </tr>
      <tr>
        <td id="L690" class="blob-num js-line-number" data-line-number="690"></td>
        <td id="LC690" class="blob-code blob-code-inner js-file-line">                         <span class=pl-k>if</span> ((<span class=pl-s>&quot;GenPart&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>var</span>.<span class=pl-s1>_name</span>) <span class=pl-c1>or</span> (<span class=pl-s>&quot;MC_&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>var</span>.<span class=pl-s1>_name</span>)) <span class=pl-c1>and</span> <span class=pl-s>&quot;Data&quot;</span> <span class=pl-c1>in</span> <span class=pl-s1>sample</span>.<span class=pl-s1>label</span>:</td>
      </tr>
      <tr>
        <td id="L691" class="blob-num js-line-number" data-line-number="691"></td>
        <td id="LC691" class="blob-code blob-code-inner js-file-line">                              <span class=pl-k>continue</span></td>
      </tr>
      <tr>
        <td id="L692" class="blob-num js-line-number" data-line-number="692"></td>
        <td id="LC692" class="blob-code blob-code-inner js-file-line">                         <span class=pl-en>plot</span>(<span class=pl-s1>lep</span>, <span class=pl-s>&#39;jets&#39;</span>, <span class=pl-s1>var</span>, <span class=pl-s1>sample</span>, <span class=pl-s1>cut_tag</span>, <span class=pl-s>&quot;&quot;</span>)</td>
      </tr>
      <tr>
        <td id="L693" class="blob-num js-line-number" data-line-number="693"></td>
        <td id="LC693" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span>(<span class=pl-s1>opt</span>.<span class=pl-s1>stack</span>):</td>
      </tr>
      <tr>
        <td id="L694" class="blob-num js-line-number" data-line-number="694"></td>
        <td id="LC694" class="blob-code blob-code-inner js-file-line">               <span class=pl-k>for</span> <span class=pl-s1>var</span> <span class=pl-c1>in</span> <span class=pl-s1>variables</span>:</td>
      </tr>
      <tr>
        <td id="L695" class="blob-num js-line-number" data-line-number="695"></td>
        <td id="LC695" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>os</span>.<span class=pl-en>system</span>(<span class=pl-s>&#39;set LD_PRELOAD=libtcmalloc.so&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L696" class="blob-num js-line-number" data-line-number="696"></td>
        <td id="LC696" class="blob-code blob-code-inner js-file-line">                    <span class=pl-en>makestack</span>(<span class=pl-s1>lep</span>, <span class=pl-s>&#39;jets&#39;</span>, <span class=pl-s1>var</span>, <span class=pl-s1>dataset_new</span>, <span class=pl-s1>cut_tag</span>, <span class=pl-s>&quot;&quot;</span>, <span class=pl-s1>lumi</span>[<span class=pl-en>str</span>(<span class=pl-s1>year</span>)])</td>
      </tr>
      <tr>
        <td id="L697" class="blob-num js-line-number" data-line-number="697"></td>
        <td id="LC697" class="blob-code blob-code-inner js-file-line">                    <span class=pl-s1>os</span>.<span class=pl-en>system</span>(<span class=pl-s>&#39;set LD_PRELOAD=libtcmalloc.so&#39;</span>)</td>
      </tr>
      <tr>
        <td id="L698" class="blob-num js-line-number" data-line-number="698"></td>
        <td id="LC698" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>if</span> <span class=pl-s1>lep</span> <span class=pl-c1>==</span> <span class=pl-s>&#39;muon&#39;</span>:</td>
      </tr>
      <tr>
        <td id="L699" class="blob-num js-line-number" data-line-number="699"></td>
        <td id="LC699" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>dataset_new</span>.<span class=pl-en>append</span>(<span class=pl-s1>sample_dict</span>[<span class=pl-s>&#39;DataEle_&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>year</span>)])</td>
      </tr>
      <tr>
        <td id="L700" class="blob-num js-line-number" data-line-number="700"></td>
        <td id="LC700" class="blob-code blob-code-inner js-file-line">          <span class=pl-k>elif</span> <span class=pl-s1>lep</span> <span class=pl-c1>==</span> <span class=pl-s>&#39;electron&#39;</span>:</td>
      </tr>
      <tr>
        <td id="L701" class="blob-num js-line-number" data-line-number="701"></td>
        <td id="LC701" class="blob-code blob-code-inner js-file-line">               <span class=pl-s1>dataset_new</span>.<span class=pl-en>append</span>(<span class=pl-s1>sample_dict</span>[<span class=pl-s>&#39;DataMu_&#39;</span><span class=pl-c1>+</span><span class=pl-en>str</span>(<span class=pl-s1>year</span>)])</td>
      </tr>
      <tr>
        <td id="L702" class="blob-num js-line-number" data-line-number="702"></td>
        <td id="LC702" class="blob-code blob-code-inner js-file-line">          </td>
      </tr>
</table>

  <details class="details-reset details-overlay BlobToolbar position-absolute js-file-line-actions dropdown d-none" aria-hidden="true">
    <summary class="btn-octicon ml-0 px-2 p-0 bg-white border border-gray-dark rounded-1" aria-label="Inline file action toolbar">
      <svg class="octicon octicon-kebab-horizontal" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M8 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM1.5 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm13 0a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path></svg>
    </summary>
    <details-menu>
      <ul class="BlobToolbar-dropdown dropdown-menu dropdown-menu-se mt-2" style="width:185px">
        <li>
          <clipboard-copy role="menuitem" class="dropdown-item" id="js-copy-lines" style="cursor:pointer;">
            Copy lines
          </clipboard-copy>
        </li>
        <li>
          <clipboard-copy role="menuitem" class="dropdown-item" id="js-copy-permalink" style="cursor:pointer;">
            Copy permalink
          </clipboard-copy>
        </li>
        <li><a class="dropdown-item js-update-url-with-hash" id="js-view-git-blame" role="menuitem" href="/adeiorio/nanoAOD-tools/blame/61fb7b8ec6e08ba888855132a00563f6ef7b22cc/python/postprocessing/makeplot.py">View git blame</a></li>
      </ul>
    </details-menu>
  </details>

  </div>

    </div>

  


  <details class="details-reset details-overlay details-overlay-dark" id="jumpto-line-details-dialog">
    <summary data-hotkey="l" aria-label="Jump to line"></summary>
    <details-dialog class="Box Box--overlay d-flex flex-column anim-fade-in fast linejump" aria-label="Jump to line">
      <!-- '"` --><!-- </textarea></xmp> --></option></form><form class="js-jump-to-line-form Box-body d-flex" action="" accept-charset="UTF-8" method="get">
        <input class="form-control flex-auto mr-3 linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" aria-label="Jump to line" autofocus>
        <button type="submit" class="btn" data-close-dialog>Go</button>
</form>    </details-dialog>
  </details>

    <div class="Popover anim-scale-in js-tagsearch-popover"
     hidden
     data-tagsearch-url="/adeiorio/nanoAOD-tools/find-definition"
     data-tagsearch-ref="master"
     data-tagsearch-path="python/postprocessing/makeplot.py"
     data-tagsearch-lang="Python"
     data-hydro-click="{&quot;event_type&quot;:&quot;code_navigation.click_on_symbol&quot;,&quot;payload&quot;:{&quot;action&quot;:&quot;click_on_symbol&quot;,&quot;repository_id&quot;:222721731,&quot;ref&quot;:&quot;master&quot;,&quot;language&quot;:&quot;Python&quot;,&quot;originating_url&quot;:&quot;https://github.com/adeiorio/nanoAOD-tools/blob/master/python/postprocessing/makeplot.py&quot;,&quot;user_id&quot;:null}}"
     data-hydro-click-hmac="6c23f0a5e753c6debda98b40f70769edf69e894a3e26a20569373cb673bb1dc0">
  <div class="Popover-message Popover-message--large Popover-message--top-left TagsearchPopover mt-1 mb-4 mx-auto Box box-shadow-large">
    <div class="TagsearchPopover-content js-tagsearch-popover-content overflow-auto" style="will-change:transform;">
    </div>
  </div>
</div>




  </div>
</div>

    </main>
  </div>

  </div>

        
<div class="footer container-xl width-full p-responsive" role="contentinfo">
  <div class="position-relative d-flex flex-row-reverse flex-lg-row flex-wrap flex-lg-nowrap flex-justify-center flex-lg-justify-between pt-6 pb-2 mt-6 f6 text-gray border-top border-gray-light ">
    <ul class="list-style-none d-flex flex-wrap col-12 col-lg-5 flex-justify-center flex-lg-justify-between mb-2 mb-lg-0">
      <li class="mr-3 mr-lg-0">&copy; 2020 GitHub, Inc.</li>
        <li class="mr-3 mr-lg-0"><a data-ga-click="Footer, go to terms, text:terms" href="https://github.com/site/terms">Terms</a></li>
        <li class="mr-3 mr-lg-0"><a data-ga-click="Footer, go to privacy, text:privacy" href="https://github.com/site/privacy">Privacy</a></li>
        <li class="mr-3 mr-lg-0"><a data-ga-click="Footer, go to security, text:security" href="https://github.com/security">Security</a></li>
        <li class="mr-3 mr-lg-0"><a href="https://githubstatus.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
        <li><a data-ga-click="Footer, go to help, text:help" href="https://docs.github.com">Help</a></li>

    </ul>

    <a aria-label="Homepage" title="GitHub" class="footer-octicon d-none d-lg-block mx-lg-4" href="https://github.com">
      <svg height="24" class="octicon octicon-mark-github" viewBox="0 0 16 16" version="1.1" width="24" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
</a>
   <ul class="list-style-none d-flex flex-wrap col-12 col-lg-5 flex-justify-center flex-lg-justify-between mb-2 mb-lg-0">
        <li class="mr-3 mr-lg-0"><a data-ga-click="Footer, go to contact, text:contact" href="https://github.com/contact">Contact GitHub</a></li>
        <li class="mr-3 mr-lg-0"><a href="https://github.com/pricing" data-ga-click="Footer, go to Pricing, text:Pricing">Pricing</a></li>
      <li class="mr-3 mr-lg-0"><a href="https://docs.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li class="mr-3 mr-lg-0"><a href="https://services.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
        <li class="mr-3 mr-lg-0"><a href="https://github.blog" data-ga-click="Footer, go to blog, text:blog">Blog</a></li>
        <li><a data-ga-click="Footer, go to about, text:about" href="https://github.com/about">About</a></li>
    </ul>
  </div>
  <div class="d-flex flex-justify-center pb-6">
    <span class="f6 text-gray-light"></span>
  </div>
</div>



  <div id="ajax-error-message" class="ajax-error-message flash flash-error">
    <svg class="octicon octicon-alert" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M8.22 1.754a.25.25 0 00-.44 0L1.698 13.132a.25.25 0 00.22.368h12.164a.25.25 0 00.22-.368L8.22 1.754zm-1.763-.707c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0114.082 15H1.918a1.75 1.75 0 01-1.543-2.575L6.457 1.047zM9 11a1 1 0 11-2 0 1 1 0 012 0zm-.25-5.25a.75.75 0 00-1.5 0v2.5a.75.75 0 001.5 0v-2.5z"></path></svg>
    <button type="button" class="flash-close js-ajax-error-dismiss" aria-label="Dismiss error">
      <svg class="octicon octicon-x" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"></path></svg>
    </button>
    You can’t perform that action at this time.
  </div>


    <script crossorigin="anonymous" async="async" integrity="sha512-bn/3rKJzBl2H64K38R8KaVcT26vKK7BJQC59lwYc+9fjlHzmy0fwh+hzBtsgTdhIi13dxjzNKWhdSN8WTM9qUw==" type="application/javascript" id="js-conditional-compat" data-src="https://github.githubassets.com/assets/compat-bootstrap-6e7ff7ac.js"></script>
    <script crossorigin="anonymous" integrity="sha512-CxjaMepCmi+z0LTeztU2S8qGD25LyHD6j9t0RSPevy63trFWJVwUM6ipAVLgtpMBBgZ53wq8JPkSeQ6ruaZL2w==" type="application/javascript" src="https://github.githubassets.com/assets/environment-bootstrap-0b18da31.js"></script>
    <script crossorigin="anonymous" async="async" integrity="sha512-NtPY+TtkSbAv3f3lo6qd7Aalc9BPwURIwf85Re39+MlkgXYeXa9qGmFlS8FlmKZ8VAjlpkIyBfpWohQjQmMVMQ==" type="application/javascript" src="https://github.githubassets.com/assets/vendor-36d3d8f9.js"></script>
    <script crossorigin="anonymous" async="async" integrity="sha512-MwOFiWexKpAMFmQ1R8v6hGSRpL7x83omQEqm1bArRTfitE/iwmdz68FuRq+tICbWGAlPx1pii5sNwhKne1M7bw==" type="application/javascript" src="https://github.githubassets.com/assets/frameworks-33038589.js"></script>
    
    <script crossorigin="anonymous" async="async" integrity="sha512-C1aKGYNguyqclWW98d2ef6rSK7S/Dolrk63xuiUM8mxAONys8ICW/1sfVnVyOuCSTr0jI241yp5AZT8ymScvWg==" type="application/javascript" src="https://github.githubassets.com/assets/behaviors-bootstrap-0b568a19.js"></script>
    
      <script crossorigin="anonymous" async="async" integrity="sha512-44qssMj+fXq3KdFy9Xwq1xbyF9+0lUDA4T8YID97FKD+j18CEaDsPGutuPP3frQFBwcikEViAK+3cFq5MzmQCg==" type="application/javascript" data-module-id="./contributions-spider-graph.js" data-src="https://github.githubassets.com/assets/contributions-spider-graph-e38aacb0.js"></script>
      <script crossorigin="anonymous" async="async" integrity="sha512-EOcKJC66ZRh9HbNcX4OaUtWMBVt6SEC3qOFS0QOam5vJQ1OD1sdHNk/Pns/CboOmqzrtBDObn7Cj06879tEsog==" type="application/javascript" data-module-id="./drag-drop.js" data-src="https://github.githubassets.com/assets/drag-drop-10e70a24.js"></script>
      <script crossorigin="anonymous" async="async" integrity="sha512-DO/rB6zRQUQMZoI04NWWxGf161OLhQbjw+MBmftXrNQeN37Q2sWHKuD/mCdFhfHN/hpHZKcMidPr7/CXdK71AQ==" type="application/javascript" data-module-id="./jump-to.js" data-src="https://github.githubassets.com/assets/jump-to-0cefeb07.js"></script>
      <script crossorigin="anonymous" async="async" integrity="sha512-+QnKFHF/C5dZacu19MfZgDmm8mM4bYgXBcTmeLyiIkJa6APeGHjqDcYjfq1FyHS4bcGxfDD/8EVQh4z+R7QSxw==" type="application/javascript" data-module-id="./profile-pins-element.js" data-src="https://github.githubassets.com/assets/profile-pins-element-f909ca14.js"></script>
      <script crossorigin="anonymous" async="async" integrity="sha512-qECv/jhsvLFN77eGNu0cjMR2+zvAlLyhQVTnmayJc5OLZoxMLjQZxZW1hK/dhcYro6Wec/aiF21HYf2N5OilYQ==" type="application/javascript" data-module-id="./randomColor.js" data-src="https://github.githubassets.com/assets/randomColor-a840affe.js"></script>
      <script crossorigin="anonymous" async="async" integrity="sha512-vK7rRnsAi4qcmC2HqCfPyEBZgIMWb6Azyb1PJxgL1FtEFMydK//dsnuLdVx+RaPGg71Z58ossFXqkLWgMevvdw==" type="application/javascript" data-module-id="./sortable-behavior.js" data-src="https://github.githubassets.com/assets/sortable-behavior-bcaeeb46.js"></script>
      <script crossorigin="anonymous" async="async" integrity="sha512-mHqsE5aQq7fAmmLd0epHBJK8rn8DOVnjW2YQOT8wvsN1oLrypw0cDFmwXPDwbMghHyo4kKiOtVJ/kEsEzwwibw==" type="application/javascript" data-module-id="./tweetsodium.js" data-src="https://github.githubassets.com/assets/tweetsodium-987aac13.js"></script>
      <script crossorigin="anonymous" async="async" integrity="sha512-+QfOLG8ES1hxkJ+lK3yX/qtYw+eNEa/t8M/3m/q/A9gu+9SJzObmbDEQLv2hiDBYx3OFx9G1a7DrxQtD5cdhEQ==" type="application/javascript" data-module-id="./user-status-submit.js" data-src="https://github.githubassets.com/assets/user-status-submit-f907ce2c.js"></script>
    
    <script crossorigin="anonymous" async="async" integrity="sha512-h+tgGlrremCjOB7LWpQ2Zw8M6RXRgCtnDV1WNZasiAOsPNZ+Lfih5uBEq/ZW44Cwx7+E2V5CAKCBXtGZ/VQDsQ==" type="application/javascript" src="https://github.githubassets.com/assets/repositories-bootstrap-87eb601a.js"></script>
<script crossorigin="anonymous" async="async" integrity="sha512-9kETUZ1VdbquV/X309o+hkBYqfPNfr2p1GtUC+utOzuDA/8GeJ/6xdcIJ0dsfndUaeXt0SOGxEem8BW6ek285Q==" type="application/javascript" src="https://github.githubassets.com/assets/github-bootstrap-f6411351.js"></script>
  <div class="js-stale-session-flash flash flash-warn flash-banner" hidden
    >
    <svg class="octicon octicon-alert" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M8.22 1.754a.25.25 0 00-.44 0L1.698 13.132a.25.25 0 00.22.368h12.164a.25.25 0 00.22-.368L8.22 1.754zm-1.763-.707c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0114.082 15H1.918a1.75 1.75 0 01-1.543-2.575L6.457 1.047zM9 11a1 1 0 11-2 0 1 1 0 012 0zm-.25-5.25a.75.75 0 00-1.5 0v2.5a.75.75 0 001.5 0v-2.5z"></path></svg>
    <span class="js-stale-session-flash-signed-in" hidden>You signed in with another tab or window. <a href="">Reload</a> to refresh your session.</span>
    <span class="js-stale-session-flash-signed-out" hidden>You signed out in another tab or window. <a href="">Reload</a> to refresh your session.</span>
  </div>
  <template id="site-details-dialog">
  <details class="details-reset details-overlay details-overlay-dark lh-default text-gray-dark hx_rsm" open>
    <summary role="button" aria-label="Close dialog"></summary>
    <details-dialog class="Box Box--overlay d-flex flex-column anim-fade-in fast hx_rsm-dialog hx_rsm-modal">
      <button class="Box-btn-octicon m-0 btn-octicon position-absolute right-0 top-0" type="button" aria-label="Close dialog" data-close-dialog>
        <svg class="octicon octicon-x" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"></path></svg>
      </button>
      <div class="octocat-spinner my-6 js-details-dialog-spinner"></div>
    </details-dialog>
  </details>
</template>

  <div class="Popover js-hovercard-content position-absolute" style="display: none; outline: none;" tabindex="0">
  <div class="Popover-message Popover-message--bottom-left Popover-message--large Box box-shadow-large" style="width:360px;">
  </div>
</div>


  </body>
</html>

