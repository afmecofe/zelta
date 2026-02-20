# Publishing Wiki to GitHub

The wiki content is ready in the `/wiki` directory. To publish it to GitHub Wiki:

## Manual Method (Recommended for First Time)

1. **Go to the repository wiki**: https://github.com/afmecofe/zelta/wiki

2. **Enable wiki** (if not already enabled):
   - Go to Settings → Features
   - Check "Wikis"

3. **Clone the wiki repository**:
   ```bash
   git clone https://github.com/afmecofe/zelta.wiki.git
   cd zelta.wiki
   ```

4. **Copy wiki content**:
   ```bash
   cp /home/ghost/Documents/github/didavie/Zelta/embedded/wiki/*.md .
   ```

5. **Commit and push**:
   ```bash
   git add *.md
   git commit -m "Initial wiki documentation"
   git push origin master
   ```

## Automated Method (GitHub Actions)

Create `.github/workflows/wiki-sync.yml` to automatically sync wiki/ directory to GitHub Wiki on every push.

## Wiki Structure

Once published, the following pages will be available:

- **Home** - Main navigation and overview
- **Quick-Start** - 15-minute getting started guide
- **Hardware-Requirements** - Supported platforms and specifications
- **Transport-MQTT** - MQTT protocol deep dive
- **FAQ** - Frequently asked questions

## Next Steps

After publishing:

1. Add more wiki pages from the Home.md navigation
2. Set up wiki navigation sidebar
3. Add images and diagrams to `/wiki/images/`
4. Enable wiki search

## Notes

- Wiki pages use kebab-case URLs (e.g., `Quick-Start.md` → `/wiki/Quick-Start`)
- The wiki is publicly readable but edit permissions can be restricted
- Consider adding a wiki sidebar for better navigation
