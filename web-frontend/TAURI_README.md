# Email Box Analyzer - Desktop App with Tauri

This project uses Tauri to create desktop applications from the Next.js web frontend.

## Prerequisites

### For Development
- Node.js 18+ and npm
- Rust (install via https://rustup.rs/)
- Platform-specific dependencies:
  - **Windows**: Microsoft Visual Studio C++ Build Tools
  - **macOS**: Xcode Command Line Tools
  - **Linux**: `build-essential`, `libwebkit2gtk-4.0-dev`, `libgtk-3-dev`, `libayatana-appindicator3-dev`, `librsvg2-dev`

### For Building
- **Windows**: Windows 10+ with Visual Studio Build Tools
- **macOS**: macOS 10.15+ with Xcode
- **Linux**: Ubuntu 18+ or equivalent

## Development

### Start the development server
```bash
npm run tauri:dev
```

This will:
1. Start the Next.js development server
2. Launch the Tauri desktop app
3. Enable hot reloading

### Build for Production

#### Build for all platforms
```bash
npm run tauri:build
```

#### Build for specific platforms
```bash
# Windows (.exe)
npm run tauri:build:win

# macOS (.dmg)
npm run tauri:build:mac

# Linux (.deb, .AppImage, etc.)
npm run tauri:build:linux
```

## Output Files

After building, you'll find the installers in:
- `src-tauri/target/release/bundle/`

### Windows
- `email-analyzer-frontend_x64-setup.exe` - Windows installer

### macOS
- `email-analyzer-frontend_x64.dmg` - macOS disk image

### Linux
- `email-analyzer-frontend_x64.deb` - Debian/Ubuntu package
- `email-analyzer-frontend_x64.AppImage` - AppImage (portable)

## Configuration

### Tauri Config (`src-tauri/tauri.conf.json`)
- Window settings (size, title, etc.)
- Permissions (file system, network, etc.)
- Build settings

### Rust Backend (`src-tauri/src/main.rs`)
- Desktop app logic
- Native API calls
- Integration with Python backend

## Integration with Python Backend

The Tauri app can communicate with your Python FastAPI backend:
1. **Development**: Connects to `http://localhost:8000`
2. **Production**: Can bundle the Python backend or connect to a deployed server

## Customization

### Icons
Replace the placeholder icons in `src-tauri/icons/` with your own:
- `32x32.png` - Small icon
- `128x128.png` - Medium icon
- `128x128@2x.png` - High DPI icon
- `icon.icns` - macOS icon
- `icon.ico` - Windows icon

### Window Settings
Modify `src-tauri/tauri.conf.json` to change:
- Window size and position
- App title and version
- Permissions and security settings

## Troubleshooting

### Common Issues
1. **Rust not found**: Install Rust via rustup.rs
2. **Build tools missing**: Install platform-specific build tools
3. **Permission errors**: Check Tauri allowlist in config

### Debug Mode
```bash
# Enable debug logging
RUST_LOG=debug npm run tauri:dev
```

## Next Steps

1. Add proper app icons
2. Integrate with Python backend API
3. Add native desktop features (notifications, file dialogs, etc.)
4. Configure code signing for distribution
5. Set up CI/CD for automated builds 